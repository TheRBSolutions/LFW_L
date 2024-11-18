from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Content
from .forms import ContentForm
import logging
from ninja import Router
from .serializers import ContentSchema
from ninja.errors import HttpError
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import ShareContentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .forms import ShareContentForm, ContentForm  # Add this import
from django.contrib.auth import get_user_model
from .models import Content, ContentShare


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
        
        # Share content
        content.share_with_email(email, request.user)
        messages.success(request, f"Content shared with {email}")
        return redirect('content:my_content')
    
    # Get shares
    shares = content.shares.all()
    
    return render(request, 'content/share.html', {
        'content': content,
        'shares': shares
    })

@login_required
@permission_required_or_403('content.can_view_shared_content', (Content, 'pk', 'pk'))
def views_view_content(request, pk):
    """View content details"""
    content = get_object_or_404(Content, pk=pk)
    return render(request, 'content/view.html', {'content': content})






# Standard Views for Template Rendering
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


@login_required
def upload_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        share_form = ShareContentForm(request.POST)  # Add the ShareContentForm to handle sharing functionality

        if form.is_valid():
            content = form.save(commit=False)
            content.user = request.user
            content.save()

            # Assign all permissions to the creator
            assign_perm('view_content', request.user, content)
            assign_perm('edit_content', request.user, content)
            assign_perm('delete_content', request.user, content)
            assign_perm('share_content', request.user, content)

            # Handle sharing functionality
            if share_form.is_valid():
                email = share_form.cleaned_data['email']
                can_edit = share_form.cleaned_data['can_edit']
                can_delete = share_form.cleaned_data['can_delete']

                try:
                    user = User.objects.get(email=email)
                    # Share content with an existing user
                    assign_perm('view_content', user, content)
                    if can_edit:
                        assign_perm('edit_content', user, content)
                    if can_delete:
                        assign_perm('delete_content', user, content)

                    # Create ContentShare record
                    ContentShare.objects.create(
                        content=content,
                        shared_by=request.user,
                        shared_with=user,
                        shared_with_email=email,
                        status='active'
                    )
                    messages.success(request, f"Content shared with {email}")
                except User.DoesNotExist:
                    # Create pending share for new user
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
                    send_mail(
                        'Invitation to Access Shared Content',
                        f'''Hello!
                        {request.user.get_full_name()} wants to share "{content.title}" with you.
                        To access this content, please register here:
                        {invitation_link}
                        ''',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=True,
                    )
                    messages.info(request, f"User with {email} does not exist. Invitation email sent.")

            messages.success(request, 'Content uploaded and shared successfully!')
            return redirect('content_list')
    else:
        form = ContentForm()
        share_form = ShareContentForm()

    return render(request, 'content/upload_content.html', {
        'form': form,
        'share_form': share_form  # Render the ShareContentForm in the template
    })




@login_required
def delete_content(request, pk):
    content = get_object_or_404(Content, pk=pk, user=request.user)
    if request.method == 'POST':
        content.delete()
        logger.info(f"Content '{content.title}' deleted by {request.user.email}")
        return redirect('content_list')
    return render(request, 'content/delete_content.html', {'content': content})





















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
