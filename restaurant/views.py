from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.context_processors import request
from django.urls import reverse
from django.views.generic import CreateView, DeleteView
from restaurant.forms import MenuForm, CategoryForm
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from restaurant.models import MenuModel, Restaurant, CategoryModel


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


class MTemplateView(TemplateView):
    template_name = 'index.html'


class MenuCreateView(LoginRequiredMixin, CreateView):
    template_name = 'admin/menu.html'
    form_class = MenuForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, "The menu was added successfully.")
        return redirect(reverse('menu:create'))

    def get_context_data(self, **kwargs):
        context = super(MenuCreateView, self).get_context_data(**kwargs)
        context['category'] = self.request.user.category.order_by('-pk')
        context['restaurant'] = self.request.user.restaurant.order_by('-pk')
        return context


class CategoryListView(ListView):
    template_name = 'admin/category.html'
    paginate_by = 10

    def get_queryset(self):
        return CategoryModel.objects.order_by('-pk')


def CategoryDelete(request):
    cat = request.POST.getlist('option')
    for i in cat:
        CategoryModel.objects.get(id=i).delete()
    return HttpResponseRedirect(reverse('menu:category'))


class CategoryCreateView(CreateView):
    template_name = 'admin/category.html'
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, "The category was added successfully.")
        return redirect(reverse('menu:category'))
