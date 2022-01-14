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
    #path('', PhotoListView.as_view(), name='list'),

    path('', MyPhotoListView.as_view(), name='myList'),

    path('tag/<slug:tag>/', PhotoTagListView.as_view(), name='tag'),

    path('<int:pk>/', PhotoDetailView.as_view(), name='detail'),

    path('create/', PhotoCreateView.as_view(), name='create'),

    path('<int:pk>/update/', PhotoUpdateView.as_view(), name='update'),

    path('<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),

    path('<int:pk>/share/', PhotoShareView.as_view(), name='share'),

    path('decrypt', DecryptionView.as_view(), name='decryptedList'),

    path('shared', SharedWithMePhotoListView.as_view(), name='sharedList'),
]
