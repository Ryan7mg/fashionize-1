from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Clothing
from .forms import ClothingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404, FileResponse
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse



@login_required
def serve_protected_media(request, username, clothing_type, filename):
    if request.user.username != username:
        raise Http404("You do not have permission to access this file.")

    # finding file name
    clothing = get_object_or_404(Clothing, owner__username=username, type=clothing_type, photo__endswith=filename)
    file_path = clothing.photo.path

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
    else:
        raise Http404("File not found.")

class ClosetListView(LoginRequiredMixin, ListView):
    model = Clothing
    context_object_name = 'clothings'
    template_name = 'closet/closet_list.html'

    def get_queryset(self):
        query_set = super().get_queryset()
        username = self.kwargs['username']
        if self.request.user.username == username:
            query_set = query_set.filter(owner=self.request.user)
        else:
            query_set = Clothing.objects.none()

        # 获取URL参数中的类型和排序选项
        clothing_type = self.request.GET.get('type', 'all')
        sort = self.request.GET.get('sort', 'created')

        # 应用类型过滤
        if clothing_type != 'all':
            query_set = query_set.filter(type=clothing_type)

        # 应用排序
        if sort == 'name':
            query_set = query_set.order_by('name')
        else:
            query_set = query_set.order_by('-created_at')

        return query_set


class ClothingCreateView(LoginRequiredMixin, CreateView):
    model = Clothing
    form_class = ClothingForm
    template_name = 'closet/clothing_form.html'
    success_url = reverse_lazy('closet:closet_list')

    def get_success_url(self):
        return reverse('closet:closet_list', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ClothingUpdateView(LoginRequiredMixin, UpdateView):
    model = Clothing
    form_class = ClothingForm
    template_name = 'closet/clothing_form.html'
    success_url = reverse_lazy('closet:closet_list')

    def get_success_url(self):
        return reverse('closet:closet_list', kwargs={'username': self.request.user.username})



@login_required
def get_clothing_items(request, username):
    if request.user.username != username:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    clothing_type = request.GET.get('type', '')
    items = Clothing.objects.filter(owner__username=username, type=clothing_type).values('id', 'name',
                                                                                         'photo')  # 假设衣物图片字段是 photo
    return JsonResponse(list(items), safe=False)

def get_item_details(request):
    item_id = request.GET.get('id')
    item_type = request.GET.get('type')  # 可选：如果您想根据类型过滤
    item = get_object_or_404(Clothing, id=item_id, type=item_type)

    # 假设 `photo` 字段是 ImageField 或 FileField
    data = {
        'name': item.name,
        'imageUrl': item.photo.url,
        'filename': item.photo.name.split('/')[-1]  # 获取文件名
    }
    return JsonResponse(data)

@login_required
@require_POST
def ajax_clothing_delete(request, username, pk):
    clothing = get_object_or_404(Clothing, pk=pk, owner=request.user)
    clothing.delete()
    return JsonResponse({"status": "success", "message": "Clothing deleted successfully"})