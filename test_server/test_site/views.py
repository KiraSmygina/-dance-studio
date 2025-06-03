from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import DanceClass, Student, Enrollment
from .forms import UserRegistrationForm, DanceClassEnrollmentForm, ContactForm, DanceClassForm
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    dance_classes = DanceClass.objects.all()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Здесь можно добавить логику отправки email или сохранения в базу
            messages.success(request, 'Ваше сообщение отправлено!')
            return redirect('index') # Перенаправляем на главную после отправки
    else:
        form = ContactForm()

    return render(request, 'test_site/index.html', {
        'dance_classes': dance_classes,
        'form': form, # Передаем форму в контекст
        'page_title': 'Главная - Танцевальная студия'
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'test_site/register.html', {
        'form': form,
        'page_title': 'Регистрация'
    })

@login_required
def profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        # Если профиль студента не существует, создаем его
        student = Student.objects.create(
            user=request.user,
            phone='Не указан',  # Значение по умолчанию
            birth_date=request.user.date_joined.date()  # Используем дату регистрации как дату рождения по умолчанию
        )
        messages.info(request, 'Профиль студента был автоматически создан. Пожалуйста, обновите свои данные.')
    
    enrollments = Enrollment.objects.filter(student=student, is_active=True)
    
    # Получаем все доступные классы для отображения в форме записи
    available_classes = DanceClass.objects.exclude(
        enrollment__student=student,
        enrollment__is_active=True
    )
    
    if request.method == 'POST':
        form = DanceClassEnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(student=student, commit=False)
            enrollment.save()
            messages.success(request, 'Вы успешно записались на класс!')
            return redirect('profile')
    else:
        form = DanceClassEnrollmentForm()
        form.fields['dance_class'].queryset = available_classes

    return render(request, 'test_site/profile.html', {
        'student': student,
        'enrollments': enrollments,
        'form': form,
        'page_title': 'Личный кабинет'
    })

@login_required
def enroll_class(request, dance_class_id=None):
    if request.method == 'POST':
        form = DanceClassEnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = request.user.student
            enrollment.save()
            messages.success(request, 'Вы успешно записались на класс!')
            return redirect('profile')
    else:
        form = DanceClassEnrollmentForm()
        # Фильтруем доступные классы для записи
        enrolled_classes = Enrollment.objects.filter(student=request.user.student, is_active=True).values_list('dance_class', flat=True)
        available_classes = DanceClass.objects.exclude(id__in=enrolled_classes)
        form.fields['dance_class'].queryset = available_classes
        
        # Если доступных классов нет, выведем сообщение
        if not available_classes.exists():
             messages.info(request, 'В данный момент нет доступных курсов для записи.')

    return render(request, 'test_site/enroll.html', {
        'form': form,
        'page_title': 'Запись на класс'
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Здесь можно добавить логику отправки email
            messages.success(request, 'Ваше сообщение отправлено!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'test_site/contact.html', {
        'form': form,
        'page_title': 'Контакты'
    })

def class_detail(request, class_id):
    dance_class = get_object_or_404(DanceClass, id=class_id)
    return render(request, 'test_site/class_detail.html', {
        'dance_class': dance_class,
        'page_title': dance_class.name
    })

def about(request):
    return render(request, 'test_site/about.html', {
        'page_title': 'О нас - Танцевальная студия'
    })

def courses(request):
    dance_classes = DanceClass.objects.all().order_by('name')
    paginator = Paginator(dance_classes, 6)  # Показываем по 6 курсов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'test_site/courses.html', {
        'page_obj': page_obj,
        'page_title': 'Курсы - Танцевальная студия'
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        student = get_object_or_404(Student, user=request.user)
        student.phone = request.POST.get('phone', student.phone)
        birth_date = request.POST.get('birth_date')
        if birth_date:
            student.birth_date = birth_date
        student.save()
        messages.success(request, 'Профиль успешно обновлен!')
    return redirect('profile')

@login_required
def cancel_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student__user=request.user)
    enrollment.is_active = False
    enrollment.save()
    messages.success(request, 'Запись на курс отменена.')
    return redirect('profile')

@staff_member_required
def add_dance_class(request):
    if request.method == 'POST':
        form = DanceClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Танцевальный класс успешно добавлен!')
            return redirect('courses') # Redirect to the courses list after adding
    else:
        form = DanceClassForm()
    
    return render(request, 'test_site/add_dance_class.html', {
        'form': form,
        'page_title': 'Добавить Танцевальный класс'
    })