from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('enroll/<int:dance_class_id>/', views.enroll_class, name='enroll_class_with_id'),
    path('enroll/', views.enroll_class, name='enroll_class'),
    path('enroll/cancel/<int:enrollment_id>/', views.cancel_enrollment, name='cancel_enrollment'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('add_class/', views.add_dance_class, name='add_dance_class'),
] 