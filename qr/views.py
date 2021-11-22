from django.http import Http404
from django.views.generic import TemplateView, ListView

from qr.models import MenuModel, Restaurant


class MTemplateView(TemplateView):
    template_name = 'index.html'


class MenuListView(ListView):
    template_name = 'user/index.html'
    model = MenuModel

    def get_queryset(self, **kwargs):
        link = self.kwargs.get('name')
        qs = Restaurant.objects.filter(link=link)
        menu = MenuModel.objects.order_by('-pk')
        if qs:
            menu = menu.filter(restaurant__link=link)
        else:
            raise Http404
        return menu




