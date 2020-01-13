from django.urls import path
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .models import Item
from .views import ItemFilterView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView
from .views import RoomFilterView, RoomDetailView, RoomCreateView, RoomUpdateView, RoomDeleteView

# アプリケーションのルーティング設定

urlpatterns = [
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    # path('', ItemFilterView.as_view(), name='index'),
    path('', RoomFilterView.as_view(), name='index'),
    path('room/detail/<int:pk>/', RoomDetailView.as_view(), name='detail'),
    path('room/update/<int:pk>/', RoomUpdateView.as_view(), name='update'),
    path('room/create/', RoomCreateView.as_view(), name='create'),
    path('room/delete/<int:pk>/', RoomDeleteView.as_view(), name='delete'),
]
