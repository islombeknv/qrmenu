from django.urls import path

from qr.views import MTemplateView, MenuListView

urlpatterns = [
    path('', MTemplateView.as_view()),
    path('menu/<str:name>/', MenuListView.as_view()),
]
