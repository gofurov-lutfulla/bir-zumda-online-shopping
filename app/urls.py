from django.urls import path
from . import views

urlpatterns = [
    path('<str:page>.html', views.legacy_html_redirect, name='legacy-html'),

    path('', views.index, name='index'),
    path('aloqa/', views.aloqa, name='aloqa'),
    path('biz-haqimizda/', views.biz_haqimizda, name='biz-haqimizda'),

    path('blog/', views.blog, name='blog'),
    path('blog-detail/<int:pk>/', views.blog_detail, name='blog-detail'),

    path('mahsulotlar/', views.mahsulotlar, name='mahsulotlar'),
    path('mahsulot-detail/<int:pk>/', views.mahsulot_detail, name='mahsulot-detail'),
    path('savatcha/', views.savatcha, name='savatcha'),
    path('checkout/', views.checkout, name='checkout'),

    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),

    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('confirm-password/', views.confirm_password, name='confirm-password'),
]