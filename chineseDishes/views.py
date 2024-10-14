from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from chineseDishes.models import Province

# Create your views here.
class ShowProvincesView(TemplateView):
    template_name = "chineseDishes/show_provinces.html"

    def get_context_data(request, *args, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['provinces'] = Province.objects.all()

        return context