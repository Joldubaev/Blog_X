from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import MyUser
from .utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, write_only=True)
    password_confirm = serializers.CharField(min_length=4, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError('Password do not match!')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code, status='register')
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                message = 'This user does not exist.'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Enter your username or password.'
            raise serializers.ValueError(message, code='authorization')

        attrs['user'] = user
        return attrs


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=1000,
                                            required=True)
    password = serializers.CharField(min_length=8,
                                     required=True)
    password_confirm = serializers.CharField(min_length=8,
                                     required=True)

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User is not found.')
        return email

    def validate_activation_code(self, act_code):
        if not MyUser.objects.filter(activation_code=act_code,
                                         is_active=False).exists():
            raise serializers.ValidationError('Invalid activation code.')
        return act_code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password mismatch.')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        activation_code = data.get('activation_code')
        password = data.get('password')
        try:
            user = MyUser.objects.get(email=email, activation_code=activation_code, is_active=False)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError('User is not found.')

        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user
