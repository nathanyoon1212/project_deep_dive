from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('reviews', include('reviews.urls')),
    path('petsitters', include('petsitters.urls')),
    path('bookings', include('bookings.urls')),
]
