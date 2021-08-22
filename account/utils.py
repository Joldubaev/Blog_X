from django.core.mail import send_mail


def send_activation_code(email, activation_code, status=None):
    if status == 'register':
        activation_url = f'http://localhost:8000/api/account/activate/{activation_code}'
        message = f"Congratulations! You are registered successfully! Follow the link to activate your account: {activation_url}"

        send_mail(
            ' Активация аккаунта',
            message,
            'admin@gmail.com',
            [email, ],
            fail_silently=False
        )

    elif status == 'reset_password':
        send_mail(
            'Сброс пароля',
            f'Ваш код активации: {activation_code}',
            'admin@gmail.com',
            [email, ],
            fail_silently=False,
        )