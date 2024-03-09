from allauth.account.forms import SignupForm
from django.core.mail import mail_managers


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        mail_managers(
            subject='Новый пользователь!',
            message=f' Пользователь {user.username} зарегистрировался на '
                    f'сайте.'
        )
        return user

# -----------------------------------------------------------------------------
# При регистрации отправляет пользователю письма со ссылкой на сайт, письмо
# имеет два формата HTML и text.

# from allauth.account.forms import SignupForm
# from django.core.mail import EmailMultiAlternatives
#
#
# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#         subject = 'Добро пожаловать в наш интернет-магазин!'
#         text = f'{user.username}, вы успешно зарегистрировались!'
#         html = (
#             f'<b>{user.username}</b>, вы успешно зарегистрировались на '
#             f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
#         )
#         msg = EmailMultiAlternatives(
#             subject=subject, body=text, from_email=None, to=[user.email]
#         )
#         msg.attach_alternative(html, "text/html")
#         msg.send()
#         return user
# -----------------------------------------------------------------------------
# При регистрации отправляет пользователю письмо

# from allauth.account.forms import SignupForm
# from django.core.mail import send_mail
#
# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#
#         send_mail(
#             subject='Добро пожаловать в наш интернет-магазин!',
#             message=f'{user.username}, вы успешно зарегистрировались!',
#             from_email=None,  # Будет использованно значение DEFAULT_FROM_EMAIL
#             recipient_list=[user.email],
#         )
#         return user
# -----------------------------------------------------------------------------
    # Эта форма при регистрации автоматически добавляет пользователя
    # в группу "common users"

# from allauth.account.forms import SignupForm
# from django.contrib.auth.models import Group

# class CustomSignupForm(SignupForm):
    # def save(self, request):
    #     user = super().save(request)
    #     common_users = Group.objects.get(name="common users")
    #     user.groups.add(common_users)
    #     return user

# -----------------------------------------------------------------------------
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )
