'''Photoapp URL patterns'''

from django.urls import path

from .views import (
    PhotoListView,
    PhotoTagListView,
    PhotoDetailView,
    PhotoCreateView,
    PhotoUpdateView,
    PhotoDeleteView,
    PhotoShareView,
    DecryptionView,
    SharedWithMePhotoListView,
    MyPhotoListView
)

app_name = 'photo'

urlpatterns = [
    path('', PhotoListView.as_view(), name='list'),

    path('photo', MyPhotoListView.as_view(), name='myList'),

    path('tag/<slug:tag>/', PhotoTagListView.as_view(), name='tag'),

    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='detail'),

    path('photo/create/', PhotoCreateView.as_view(), name='create'),

    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='update'),

    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),

    path('photo/<int:pk>/share/', PhotoShareView.as_view(), name='share'),

    path('decrypt', DecryptionView.as_view(), name='decryptedList'),

    path('shared', SharedWithMePhotoListView.as_view(), name='sharedList'),
]
