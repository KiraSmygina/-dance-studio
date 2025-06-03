from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DanceClass(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название класса')
    description = models.TextField(verbose_name='Описание')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name='Уровень')
    instructor = models.CharField(max_length=100, verbose_name='Инструктор')
    schedule = models.CharField(max_length=100, verbose_name='Расписание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    max_students = models.IntegerField(verbose_name='Максимальное количество студентов')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_level_display()}"

    class Meta:
        verbose_name = 'Танцевальный класс'
        verbose_name_plural = 'Танцевальные классы'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    birth_date = models.DateField(verbose_name='Дата рождения')
    dance_classes = models.ManyToManyField(DanceClass, through='Enrollment', verbose_name='Танцевальные классы')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    dance_class = models.ForeignKey(DanceClass, on_delete=models.CASCADE, verbose_name='Танцевальный класс')
    enrollment_date = models.DateTimeField(default=timezone.now, verbose_name='Дата записи')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f"{self.student} - {self.dance_class}"

    class Meta:
        verbose_name = 'Запись на класс'
        verbose_name_plural = 'Записи на классы'
        unique_together = ('student', 'dance_class')
