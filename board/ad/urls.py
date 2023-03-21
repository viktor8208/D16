from django.contrib import admin
from django.urls import path, include
from .views import AdList, AdUserList, AdUserCreate, AdUserUpdate, AdUserDelete, UserResponseCreate, UserResponseList
from .views import UserResponseUpdate, UserResponseDelete, AdDetail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', AdList.as_view(), name='ad_list'),

    path('user', AdUserList.as_view(), name='ad_user_list'),
    path('create', AdUserCreate.as_view(), name='ad_create'),
    path('<int:pk>', AdDetail.as_view(), name='ad_detail'),
    path('<int:pk>/update/', AdUserUpdate.as_view(), name='ad_update'),
    path('<int:pk>/delete/', AdUserDelete.as_view(), name='ad_delete'),
    path('<int:pk>/ur_create', UserResponseCreate.as_view(), name='ur_create'),
#    path('ur_list', UserResponseList.as_view(), name='ur_list'),
    path('ur_list/<int:pk>/ur_update', UserResponseUpdate.as_view(), name='ur_update'),
    path('ur_list/<int:pk>/ur_delete', UserResponseDelete.as_view(), name='ur_delete'),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
