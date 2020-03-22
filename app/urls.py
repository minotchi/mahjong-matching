from django.urls import path
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .models import Item
from .views import LoginView, ItemFilterView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView
from .views import RoomFilterView, RoomDetailView, RoomCreateView, RoomUpdateView, RoomDeleteView, RoomJoinRequestCreateView, RoomJoinRequestFilterView, RoomUserCreateView, CommentFilterView, CommentCreateView, OshihikiFilterView

# アプリケーションのルーティング設定

urlpatterns = [
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    path('item', ItemFilterView.as_view(), name='item_index'),
    path('', RoomFilterView.as_view(), name='index'),
    path('room/detail/<int:pk>/', RoomDetailView.as_view(), name='detail'),
    path('room/join_request/<int:pk>/',
         RoomJoinRequestCreateView.as_view(), name='join_request'),
    path('room/update/<int:pk>/', RoomUpdateView.as_view(), name='update'),
    path('room/create/', RoomCreateView.as_view(), name='create'),
    path('room/delete/<int:pk>/', RoomDeleteView.as_view(), name='delete'),
    path('room_join_request/<int:pk>/', RoomJoinRequestFilterView.as_view(), name='room_join_request'),
    path('room_join_request/<int:pk>/approve/', RoomUserCreateView.as_view(), name='roomjoinrequest_approve'),
    path('talk/<int:pk>/',
         CommentFilterView.as_view(), name='talk'),
    path('talk/<int:pk>/create/',
         CommentCreateView.as_view(), name='comment_create'),

    path('oshihiki/', OshihikiFilterView.as_view(), name='oshihiki'),
]
