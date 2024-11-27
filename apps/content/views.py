from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Content
from .forms import ContentUploadForm
import logging
from ninja import Router
from .serializers import ContentSchema
from ninja.errors import HttpError
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import ShareContentForm
from django.shortcuts import get_object_or_404, render, redirect
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import ContentShare
from django.db import IntegrityError
from filer.models import Folder, File
from .forms import FolderForm
from django.contrib.admin.views.decorators import staff_member_required


User = get_user_model()





logger = logging.getLogger(__name__)


@login_required
def views_my_content(request):
    """List user's owned and shared content"""
    owned_content = Content.objects.filter(user=request.user)
    shared_content = get_objects_for_user(
        request.user,
        'content.view_content'
    ).exclude(user=request.user)
    
    return render(request, 'content/my_content.html', {
        'owned_content': owned_content,
        'shared_content': shared_content
    })


@login_required
@permission_required_or_403('content.can_share_content', (Content, 'pk', 'pk'))
def share_content(request, pk):
    """Share content with other users"""
    content = get_object_or_404(Content, pk=pk)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if already shared
        if ContentShare.objects.filter(content=content, shared_with_email=email).exists():
            messages.warning(request, f"Content already shared with {email}")
            return redirect('content:share', pk=pk)
        
        # Share content via email
        content.share_with_email(email, request.user)
        messages.success(request, f"Content shared with {email}")
        return redirect('content:my_content')
    
    # Fetch all shares for the content
    shares = content.shares.all()
    
    return render(request, 'content/share.html', {
        'content': content,
        'shares': shares
    })
# @login_required
# @permission_required_or_403('content.can_share_content', (Content, 'pk', 'pk'))
# def share_content(request, pk):
#     """Share content with other users"""
#     content = get_object_or_404(Content, pk=pk)
    
#     if request.method == 'POST':
#         email = request.POST.get('email')
        
#         # Check if already shared
#         if ContentShare.objects.filter(content=content, shared_with_email=email).exists():
#             messages.warning(request, f"Content already shared with {email}")
#             return redirect('content:share', pk=pk)
        
#         # Share content
#         content.share_with_email(email, request.user)
#         messages.success(request, f"Content shared with {email}")
#         return redirect('content:my_content')
    
#     # Get shares
#     shares = content.shares.all()
    
#     return render(request, 'content/share.html', {
#         'content': content,
#         'shares': shares
#     })



@login_required
@permission_required_or_403('content.can_view_shared_content', (Content, 'pk', 'pk'))
def views_view_content(request, pk):
    """View content details"""
    content = get_object_or_404(Content, pk=pk)
    return render(request, 'content/view.html', {'content': content})

# @login_required
# @permission_required_or_403('content.can_view_shared_content', (Content, 'pk', 'pk'))
# def views_view_content(request, pk):
#     """View content details"""
#     content = get_object_or_404(Content, pk=pk)
#     return render(request, 'content/view.html', {'content': content})








@login_required
def content_list(request):
    """List only content the user has permission to view."""
    contents = get_objects_for_user(request.user, 'content.view_content')
    own_content = contents.filter(user=request.user)
    shared_content = contents.exclude(user=request.user)

    return render(request, 'content/content_list.html', {
        'own_content': own_content,
        'shared_content': shared_content
    })


# Standard Views for Template Rendering
# @login_required
# def content_list(request):
#     """List only content the user has permission to view."""
#     contents = get_objects_for_user(request.user, 'content.view_content')
#     own_content = contents.filter(user=request.user)
#     shared_content = contents.exclude(user=request.user)

#     return render(request, 'content/content_list.html', {
#         'own_content': own_content,
#         'shared_content': shared_content
#     })



@staff_member_required  # Restrict access to staff/admin users only
def upload_content(request, folder_id=None):
    """Allows staff to upload content and optionally share it."""
    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id)

    if request.method == 'POST':
        form = ContentUploadForm(request.user, request.POST, request.FILES)
        share_form = ShareContentForm(request.POST)

        if form.is_valid():
            # Save content
            content = form.save(commit=False)
            content.user = request.user
            if folder:
                content.folder = folder
            content.save()

            # Assign default permissions to content owner
            assign_perm('view_content', request.user, content)

            # Handle sharing functionality
            if share_form.is_valid() and share_form.cleaned_data.get('email'):
                email = share_form.cleaned_data['email']
                can_edit = share_form.cleaned_data['can_edit']
                can_delete = share_form.cleaned_data['can_delete']

                try:
                    # Check if the user already exists
                    user = User.objects.get(email=email)

                    # Assign permissions to the existing user
                    assign_perm('view_content', user, content)
                    if can_edit:
                        assign_perm('edit_content', user, content)
                    if can_delete:
                        assign_perm('delete_content', user, content)

                    # Record the sharing
                    ContentShare.objects.create(
                        content=content,
                        shared_by=request.user,
                        shared_with=user,
                        shared_with_email=email,
                        status='active'
                    )
                    messages.success(request, f"Content shared with {email}")

                except User.DoesNotExist:
                    # Handle sharing for non-existing users
                    invitation_token = uuid.uuid4().hex
                    ContentShare.objects.create(
                        content=content,
                        shared_by=request.user,
                        shared_with_email=email,
                        status='pending',
                        invitation_token=invitation_token
                    )

                    # Send invitation email
                    invitation_link = f"{settings.SITE_URL}/register/?token={invitation_token}"
                    success = send_invitation_email(
                        email=email,
                        invitation_link=invitation_link,
                        content_title=content.title,
                        inviter_name=request.user.get_full_name()
                    )
                    if success:
                        messages.info(request, f"Invitation sent to {email}.")
                    else:
                        messages.error(request, f"Failed to send invitation to {email}. Please try again.")

            messages.success(request, 'Content uploaded successfully!')
            return redirect('admin:filer_folder_changelist')

    else:
        form = ContentUploadForm(request.user)
        share_form = ShareContentForm()

    return render(request, 'admin/content/upload_content_admin.html', {
        'form': form,
        'share_form': share_form,
        'folder': folder
    })


# @login_required
# def upload_content(request, folder_id=None):
#     # Fetch folder if a folder_id is provided
#     folder = None
#     if folder_id:
#         folder = get_object_or_404(Folder, id=folder_id, user=request.user)

#     if request.method == 'POST':
#         form = ContentForm(request.POST, request.FILES)
#         share_form = ShareContentForm(request.POST)  # Form to handle sharing functionality

#         if form.is_valid():
#             content = form.save(commit=False)
#             content.user = request.user

#             # Associate with a folder if provided
#             if folder:
#                 content.folder = folder

#             content.save()

#             # Assign permissions to the creator
#             assign_perm('view_content', request.user, content)
#             assign_perm('edit_content', request.user, content)
#             assign_perm('delete_content', request.user, content)
#             assign_perm('share_content', request.user, content)

#             # Handle sharing if the share form is valid
#             if share_form.is_valid():
#                 email = share_form.cleaned_data['email']
#                 can_edit = share_form.cleaned_data['can_edit']
#                 can_delete = share_form.cleaned_data['can_delete']

#                 try:
#                     user = User.objects.get(email=email)
#                     # Assign permissions to an existing user
#                     assign_perm('view_content', user, content)
#                     if can_edit:
#                         assign_perm('edit_content', user, content)
#                     if can_delete:
#                         assign_perm('delete_content', user, content)

#                     # Create a record for content sharing
#                     ContentShare.objects.create(
#                         content=content,
#                         shared_by=request.user,
#                         shared_with=user,
#                         shared_with_email=email,
#                         status='active'
#                     )
#                     messages.success(request, f"Content shared with {email}")

#                 except User.DoesNotExist:
#                     # Handle case when the user doesn't exist
#                     invitation_token = uuid.uuid4().hex
#                     ContentShare.objects.create(
#                         content=content,
#                         shared_by=request.user,
#                         shared_with_email=email,
#                         status='pending',
#                         invitation_token=invitation_token
#                     )

#                     # Send an invitation email
#                     invitation_link = f"{settings.SITE_URL}/register/?token={invitation_token}"
#                     send_mail(
#                         'Invitation to Access Shared Content',
#                         f'''Hello!
#                         {request.user.get_full_name()} wants to share "{content.title}" with you.
#                         To access this content, please register here:
#                         {invitation_link}
#                         ''',
#                         settings.DEFAULT_FROM_EMAIL,
#                         [email],
#                         fail_silently=True,
#                     )
#                     messages.info(request, f"User with {email} does not exist. Invitation email sent.")

#             messages.success(request, 'Content uploaded and shared successfully!')
#             return redirect('content_list')
#     else:
#         form = ContentForm()
#         share_form = ShareContentForm()

#     return render(request, 'content/upload_content.html', {
#         'form': form,
#         'share_form': share_form,  # Render the ShareContentForm in the template
#         'folder': folder  # Pass folder context to the template
#     })


@login_required
def delete_content(request, pk):
    content = get_object_or_404(Content, pk=pk, user=request.user)
    if request.method == 'POST':
        content.delete()
        logger.info(f"Content '{content.title}' deleted by {request.user.email}")
        return redirect('content_list')
    return render(request, 'content/delete_content.html', {'content': content})





# @login_required
# def folder_list(request):
#     """View to list all folders and their contents"""
#     root_folders = Folder.objects.filter(user=request.user, parent=None)
#     return render(request, 'content/folder_list.html', {
#         'root_folders': root_folders
#     })


@staff_member_required  # Restrict access to staff/admin users only
def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    # Fetch subfolders and files
    subfolders = Folder.objects.filter(parent=folder)
    files = File.objects.filter(folder=folder)

    return render(request, 'admin/content/folder_detail_admin.html', {
        'folder': folder,
        'subfolders': subfolders,
        'files': files
    })



@login_required
def folder_list(request):
    # List folders for the current user (or customize as needed)
    folders = Folder.objects.all()
    return render(request, 'content/folder_list.html', {'folders': folders})

@login_required
def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        parent_folder = None
        if parent_id:
            parent_folder = get_object_or_404(Folder, id=parent_id)

        Folder.objects.create(
            name=folder_name,
            owner=request.user,  # If your setup uses owner (make sure this matches your config)
            parent=parent_folder
        )
        return redirect('folder_list')

    return render(request, 'content/create_folder.html')




@login_required
def delete_folder(request, folder_id):
    """Delete folder and its contents"""
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    parent_id = folder.parent.id if folder.parent else None
    
    if request.method == 'POST':
        folder.delete()
        messages.success(request, 'Folder deleted successfully!')
        if parent_id:
            return redirect('folder_detail', folder_id=parent_id)
        return redirect('folder_list')
    
    return render(request, 'content/folder_confirm_delete.html', {'folder': folder})















# Ninja Router Setup
router = Router()

# List Content Endpoint (GET)
@router.get('/content', response=list[ContentSchema])
def list_content(request):
    logger.debug("Fetching content for user")
    return Content.objects.filter(user=request.user)

# Create Content Endpoint (POST)
@router.post('/content', response=ContentSchema)
def create_content(request, content: ContentSchema):
    logger.debug(f"Creating content with title '{content.title}' for user {request.user.email}")
    content_instance = Content.objects.create(**content.dict(), user=request.user)
    return content_instance

# Retrieve Content by ID Endpoint (GET)
@router.get('/content/{content_id}', response=ContentSchema)
def get_content(request, content_id: int):
    content = get_object_or_404(Content, pk=content_id, user=request.user)
    logger.debug(f"Fetching content '{content.title}' for user {request.user.email}")
    return content

# # Update Content Endpoint (PUT)
# @router.put('/content/{content_id}', response=ContentSchema)
# def update_content(request, content_id: int, data: ContentSchema):
#     content = get_object_or_404(Content, pk=content_id, user=request.user)
#     logger.debug(f"Updating content '{content.title}' for user {request.user.email}")
#     for attr, value in data.dict().items():
#         setattr(content, attr, value)
#     content.save()
#     return content

# # Delete Content Endpoint (DELETE)
# @router.delete('/content/{content_id}', response={})
# def delete_content_api(request, content_id: int):
#     content = get_object_or_404(Content, pk=content_id, user=request.user)
#     logger.info(f"Deleting content '{content.title}' by user {request.user.email}")
#     content.delete()
#     return {"success": True}
