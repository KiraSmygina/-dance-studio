from django.contrib import admin
from .models import DanceClass, Student, Enrollment

@admin.register(DanceClass)
class DanceClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'instructor', 'schedule', 'price', 'max_students')
    list_filter = ('level', 'instructor')
    search_fields = ('name', 'description', 'instructor')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'dance_class', 'enrollment_date', 'is_active')
    list_filter = ('is_active', 'enrollment_date')
    search_fields = ('student__user__username', 'dance_class__name')
