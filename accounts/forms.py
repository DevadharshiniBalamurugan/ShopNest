from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Address,Profile

class RegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)
    role=forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    class Meta: model=User; fields=['first_name','last_name','username','email','role','password1','password2']
    def clean_email(self):
        email=self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists(): raise forms.ValidationError('An account with this email already exists.')
        return email

class UserEditForm(forms.ModelForm):
    class Meta: model=User; fields=['first_name','last_name','email']
class ProfileForm(forms.ModelForm):
    class Meta: model=Profile; fields=['phone','bio','avatar']
class AddressForm(forms.ModelForm):
    class Meta: model=Address; fields=['full_name','phone','address','city','state','postal_code','country','is_default']

for form_class in [RegisterForm,UserEditForm,ProfileForm,AddressForm]:
    for field in form_class.base_fields.values(): field.widget.attrs['class']='form-input'
