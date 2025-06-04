from django.contrib import admin
from django.urls import path
from socialmedia import settings
from userauth import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),
    path('loginn/',views.loginn),
    path('signup/',views.signup),
    path('logoutt/',views.logoutt),
    path('upload',views.upload),
    path('like-post/<str:id>', views.likes, name='like-post'),
    path('#<str:id>', views.home_post),
    path('explore',views.explore),
    path('profile/<str:id_user>', views.profile),
    path('delete/<str:id>', views.delete),
    path('search-results/', views.search_results, name='search_results'),
    path('follow', views.follow, name='follow'),
    
    # Community URLs
    path('communities/', views.communities_list, name='communities_list'),
    path('communities/<uuid:community_id>/', views.community_detail, name='community_detail'),
    path('communities/create/', views.create_community, name='create_community'),
    path('communities/<uuid:community_id>/join/', views.join_community, name='join_community'),
    path('communities/<uuid:community_id>/leave/', views.leave_community, name='leave_community'),
    path('communities/<uuid:community_id>/post/', views.create_community_post, name='create_community_post'),
]
