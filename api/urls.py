from django.urls import path

from .import views

urlpatterns = [
    path('create/<str:audioType>/', views.CreateView.as_view(), name='create'),
    path('update/<str:audioType>/<int:audioFileID>/', views.UpdateView.as_view(), name='update'),
    path('read/<str:audioType>/', views.ReadView.as_view(), name='list'),
    path('read/<str:audioType>/<int:audioFileID>/', views.ReadView.as_view(), name='read'),
    path('delete/<str:audioType>/<int:audioFileID>/', views.DeleteView.as_view(), name='delete')
]
