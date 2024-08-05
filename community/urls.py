from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]
