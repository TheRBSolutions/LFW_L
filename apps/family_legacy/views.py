# apps/family_legacy/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FamilyLegacy
from .forms import FamilyLegacyForm
import logging
from ninja import Router
from .serializers import FamilyLegacySchema
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

# Standard Views for Template Rendering
@login_required
def legacy_list(request):
    legacies = FamilyLegacy.objects.filter(user=request.user)
    return render(request, 'family_legacy/legacy_list.html', {'legacy_list': legacies})

@login_required
def add_legacy(request):
    if request.method == 'POST':
        form = FamilyLegacyForm(request.POST)
        if form.is_valid():
            legacy = form.save(commit=False)
            legacy.user = request.user
            legacy.save()
            logger.info(f"Legacy '{legacy.title}' added by {request.user.email}")
            return redirect('legacy_list')
    else:
        form = FamilyLegacyForm()
    return render(request, 'family_legacy/add_legacy.html', {'form': form})

# Ninja Router Setup
router = Router()

# List Family Legacies Endpoint (GET)
@router.get('/family_legacy', response=list[FamilyLegacySchema])
def list_family_legacy(request):
    logger.debug(f"Fetching all family legacy records for user {request.user.email}")
    return FamilyLegacy.objects.filter(user=request.user)

# Create Family Legacy Endpoint (POST)
@router.post('/family_legacy', response=FamilyLegacySchema)
def create_family_legacy(request, legacy: FamilyLegacySchema):
    logger.debug(f"Adding family legacy '{legacy.title}' for user {request.user.email}")
    legacy_instance = FamilyLegacy.objects.create(**legacy.dict(), user=request.user)
    return legacy_instance

# Retrieve Family Legacy by ID Endpoint (GET)
@router.get('/family_legacy/{legacy_id}', response=FamilyLegacySchema)
def get_family_legacy(request, legacy_id: int):
    legacy = get_object_or_404(FamilyLegacy, pk=legacy_id, user=request.user)
    logger.debug(f"Fetching family legacy '{legacy.title}' for user {request.user.email}")
    return legacy

# Update Family Legacy Endpoint (PUT)
@router.put('/family_legacy/{legacy_id}', response=FamilyLegacySchema)
def update_family_legacy(request, legacy_id: int, data: FamilyLegacySchema):
    legacy = get_object_or_404(FamilyLegacy, pk=legacy_id, user=request.user)
    logger.debug(f"Updating family legacy '{legacy.title}' for user {request.user.email}")
    for attr, value in data.dict().items():
        setattr(legacy, attr, value)
    legacy.save()
    return legacy

# Delete Family Legacy Endpoint (DELETE)
@router.delete('/family_legacy/{legacy_id}', response={})
def delete_family_legacy(request, legacy_id: int):
    legacy = get_object_or_404(FamilyLegacy, pk=legacy_id, user=request.user)
    logger.info(f"Deleting family legacy '{legacy.title}' by user {request.user.email}")
    legacy.delete()
    return {"success": True}
