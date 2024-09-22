# accounts/forms.py


from django import forms
from .models import Listing


class ListingForm(forms.Form):
    class Meta:
        model = Listing
        fields = ['seller', 'title', 'description', 'phone_number', 'email', 'address', 'city', 'state', 'zip_code', 'price',
                  'bedrooms', 'bathrooms', 'square_feet', 'year_built', 'photo_main', 'photo_1', 'photo_2', 'photo_3',
                  'photo_4', 'photo_5', 'photo_6', 'is_published', 'list_date']
        

class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=150, label='Full Name')
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15, required=False)
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

# forms.py
from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


from .models import Inquiry

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone_number', 'message']

class PropertySearchForm(forms.Form):
    city = forms.CharField(required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    bathrooms = forms.IntegerField(required=False)