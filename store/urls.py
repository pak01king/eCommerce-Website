from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .custom_auth import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('produse/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('register-login/', views.register_login, name='register_login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('activate/<int:uid>/<str:token>/', views.activate_account, name='activate_account'),
    path('profil/', views.profile_view, name='profile'),
    path('suport/', views.suport, name='suport'),
]
