from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Content
from .forms import ContentForm
import logging
from ninja import Router
from .serializers import ContentSchema
from ninja.errors import HttpError

logger = logging.getLogger(__name__)

# Standard Views for Template Rendering
@login_required
def content_list(request):
    contents = Content.objects.filter(user=request.user)
    return render(request, 'content/content_list.html', {'content_list': contents})

@login_required
def upload_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.user = request.user
            content.save()
            logger.info(f"Content '{content.title}' uploaded by {request.user.email}")
            return redirect('content_list')
    else:
        form = ContentForm()
    return render(request, 'content/upload_content.html', {'form': form})

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

# Update Content Endpoint (PUT)
@router.put('/content/{content_id}', response=ContentSchema)
def update_content(request, content_id: int, data: ContentSchema):
    content = get_object_or_404(Content, pk=content_id, user=request.user)
    logger.debug(f"Updating content '{content.title}' for user {request.user.email}")
    for attr, value in data.dict().items():
        setattr(content, attr, value)
    content.save()
    return content

# Delete Content Endpoint (DELETE)
@router.delete('/content/{content_id}', response={})
def delete_content_api(request, content_id: int):
    content = get_object_or_404(Content, pk=content_id, user=request.user)
    logger.info(f"Deleting content '{content.title}' by user {request.user.email}")
    content.delete()
    return {"success": True}
