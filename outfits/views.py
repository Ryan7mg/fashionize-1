import os
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseNotAllowed, Http404, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from fashionize import settings
from .models import Outfit
from django.urls import reverse_lazy, reverse
from .forms import OutfitForm


class OutfitListView(LoginRequiredMixin, ListView):
    model = Outfit
    context_object_name = 'outfits'
    template_name = 'outfits/my_outfits.html'

    def get_queryset(self):
        query_set = super().get_queryset().filter(owner=self.request.user)
        sort = self.request.GET.get('sort', 'name')

        if sort == 'created_at':
            query_set = query_set.order_by('-created_at')
        else:  # 默认按名称排序
            query_set = query_set.order_by('name')

        return query_set





class OutfitCreateView(CreateView):
        model = Outfit
        form_class = OutfitForm
        template_name = 'outfits/create_outfit.html'

        def form_valid(self, form):
            form.instance.owner = self.request.user
            # 直接保存表单，不需要调用 process_and_synthesize_images
            response = super().form_valid(form)
            return response

        def get_success_url(self):
            # 动态生成重定向URL，确保包含用户名
            username = self.request.user.username
            return reverse('outfits:my_outfits', kwargs={'username': username})


def delete_outfit(request, username, pk):
    if request.method == 'POST':
        outfit = get_object_or_404(Outfit, pk=pk, owner=request.user)
        outfit.delete()
        return JsonResponse({'status': 'success', 'message': 'Outfit deleted successfully'})
    else:
        return HttpResponseNotAllowed(['POST'])

class OutfitUpdateView(LoginRequiredMixin, UpdateView):
    model = Outfit
    form_class = OutfitForm
    template_name = 'outfits/update_outfit.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Outfit, pk=pk, owner=self.request.user)

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('outfits:my_outfits', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        outfit = self.get_object()
        context['top_image_url'] = outfit.top.image.url if outfit.top else ''
        context['bottom_image_url'] = outfit.bottom.image.url if outfit.bottom else ''
        context['shoe_image_url'] = outfit.shoe.image.url if outfit.shoe else ''
        return context


@login_required
def serve_protected_media(request, username, filename):
    if request.user.username != username:
        raise Http404("You do not have permission to access this file.")

    # Check if the request is for outfit images
    if 'outfit_images' in filename:
        # The path for outfit images
        file_path = os.path.join(settings.MEDIA_ROOT, username, 'outfit_images', filename)
    else:
        # The path for clothing images (top, bottom, shoe)
        file_path = os.path.join(settings.MEDIA_ROOT, username, filename)

    if os.path.exists(file_path):
        # Return the file if it exists
        return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
    else:
        # If the file does not exist, return a 404 error
        raise Http404("File not found.")
