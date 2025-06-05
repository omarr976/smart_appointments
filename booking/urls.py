from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),  # page d'accueil = login

    path('my-account/', views.my_account, name='my_account'),
    path('about-us/', views.about_us, name='about_us'),

    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

    path('home/', views.home, name='home'),  # on garde home accessible ici

    path('book/<int:service_id>/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),

    path('accounts/', include('django.contrib.auth.urls')),
]
