from datetime import datetime

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from closet.models import Clothing
from outfits.models import Outfit
from fashionize import settings
import requests


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        # 确保请求的用户名匹配当前登录的用户
        if request.user.username != username:
            raise Http404("Dashboard not found.")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        query = 'fashion'
        date_from = datetime.now().date().isoformat()
        news_api_url = f'https://newsapi.org/v2/everything?q={query}&from={date_from}&sortBy=publishedAt&apiKey={settings.NEWS_API_KEY}'

        # 发起请求
        response = requests.get(news_api_url)
        if response.status_code == 200:

            news_data = response.json()

            recent_news = news_data.get('articles', [])[:5]
            context['recent_news'] = recent_news
        else:
            print(f"Failed to fetch news: {response.status_code}")
            context['recent_news'] = []


        recent_outfits = Outfit.objects.filter(owner=self.request.user).order_by('-created_at')[:5]
        context['recent_outfits'] = recent_outfits
        recent_clothings = Clothing.objects.order_by('-created_at')[:5]
        context['recent_clothings'] = recent_clothings
        context['username'] = self.kwargs.get('username')
        return context

