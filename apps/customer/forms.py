from django import forms
from apps.customer.models import Address
from apps.core.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserRegistrationForm(forms.Form):
    """
        Form For User Registration
    """
    gender_choices = (
        ('male', 'مذکر'),
        ('female', 'مونث')
    )
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), validators=[validate_password])
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), validators=[validate_password])

    def clean_phone(self):
        """
            Validate phone being unique
        """
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise ValidationError('This Phone Number already exists !')
        else:
            return phone

    def clean_email(self):
        """
            Validate email being unique
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This Email already exists !')
        else:
            return email

    def clean(self):
        """
            Validate Password and Confirm being Match
        """
        clean_data = super().clean()
        password = clean_data.get('password1')
        confirm = clean_data.get('password2')

        if password and confirm and password != confirm:
            raise ValidationError('Password is not match !')


class UserLoginForm(forms.Form):
    """
        Form For User Login
    """
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserAddressForm(forms.ModelForm):
    model = Address
    fields = ['city', 'postal_code', 'address']