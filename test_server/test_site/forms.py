from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, DanceClass, Enrollment

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    phone = forms.CharField(required=True, label='Телефон')
    birth_date = forms.DateField(required=True, label='Дата рождения', 
                               widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'password1', 'password2')
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        help_texts = {
            'username': 'Обязательное поле. 150 символов или меньше. Только буквы, цифры и @/./+/-/_',
            'password1': 'Ваш пароль должен содержать как минимум 8 символов.',
            'password2': 'Введите тот же пароль, что и выше, для подтверждения.',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                birth_date=self.cleaned_data['birth_date']
            )
        return user

class DanceClassEnrollmentForm(forms.ModelForm):
    dance_class = forms.ModelChoiceField(
        queryset=DanceClass.objects.all(),
        label='Выберите класс для записи'
    )

    class Meta:
        model = Enrollment
        fields = ['dance_class']

    def save(self, student, commit=True):
        dance_class = self.cleaned_data['dance_class']
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            dance_class=dance_class,
            defaults={'is_active': True}
        )
        if not created:
            enrollment.is_active = True
            enrollment.save()

        if commit:
            # In a ModelForm, save() without commit=False typically saves the main object.
            # Since we are creating/updating Enrollment instances manually, 
            # we don't need to call super().save() here.
            pass

        return enrollment

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, required=True, label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=True, label='Сообщение')

class DanceClassForm(forms.ModelForm):
    class Meta:
        model = DanceClass
        fields = ['name', 'description', 'level', 'instructor', 'schedule', 'price', 'max_students']
        labels = {
            'name': 'Название класса',
            'description': 'Описание',
            'level': 'Уровень',
            'instructor': 'Инструктор',
            'schedule': 'Расписание',
            'price': 'Цена',
            'max_students': 'Максимальное количество студентов',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        } 