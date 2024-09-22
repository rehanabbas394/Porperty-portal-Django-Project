# accounts/urls.py

from django.urls import path
from . import views 
from .views import custom_login_view
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('login/', views.custom_login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.buyer_dashboard, name='buyer_dashboard'),
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    
    path('login/', custom_login_view, name='custom_login'),  # Define the URL pattern with a name
    # path('', views.home_view, name='home'),
    path('add_listing/', views.add_listing, name='add_listing'),
    path('book_listing/<int:listing_id>/', views.book_listing, name='book_listing'),
    path('edit_listing/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('delete_listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path('logout/', views.custom_logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('listing/<int:listing_id>/', views.listing_detail_view, name='listing_detail'),
    path('contact/', views.contact_us, name='contact_us'),
    path('success/', views.success_page, name='success_page'),
    path('search/', views.search_listings, name='search_listings'),
]