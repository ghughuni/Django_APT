from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_url", views.add_url, name="add_url"),
    path("delete_url/<int:id>", views.delete_url, name="delete_url"),
    path("update_url", views.update_url, name="update_url"),
    
    # API
    path('api_links/', views.links_list, name='links_list'),
    path('link_details/<int:pk>/', views.link_details, name='link_details'),
    path('link_delete/<int:pk>/', views.link_delete, name='link_delete'),
]