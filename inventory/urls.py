from django.contrib import admin
from django.urls import path
# from .views import  RegisterUser, LoginUser
from django.contrib.auth import views as auth_views
from .views import register_user,login_user,create_item, get_item, update_item, delete_item,get_all_items
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('', Index.as_view(), name='index'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('items/', create_item, name='create-item'),
    path('items/all/', get_all_items, name='get-all-items'), 
    path('items/<int:item_id>/', get_item, name='get-item'),
    path('items/<int:item_id>/update/', update_item, name='update-item'),
    path('items/<int:item_id>/delete/', delete_item, name='delete-item'),
    
]

