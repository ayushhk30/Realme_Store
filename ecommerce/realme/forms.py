from django import forms 
from . models import Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

class OrderCreateForm(forms.ModelForm): 
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'pincode', 'city']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']