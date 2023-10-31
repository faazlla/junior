from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	


from .models import Language

class SearchForm(forms.Form):
    Language = forms.ModelChoiceField(queryset=Language.objects.all(), empty_label="Select Language")
    Rating = forms.IntegerField(min_value=0, max_value=5, widget=forms.NumberInput(attrs={'type': 'number'}))
    NumRatings = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'type': 'number'}))


from .models import Junior


class JuniorRegistrationForm(forms.ModelForm):
    primarni_jezik = forms.ModelChoiceField(queryset=Language.objects.all(), empty_label="Select Language")

    class Meta:
        model = Junior
        fields = ['ime_i_prezime', 'primarni_jezik', 'email', 'broj_telefona', 'kratak_opis', 'dodatni_it_skilovi', 'git_link', 'linkedin_link', 'portfolio_link', 'pdf_cv', 'image']


from django import forms

class OcjenaForm(forms.Form):
    ocjena = forms.IntegerField(
        label='Ocijenite juniora:',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'type': 'number', 'required': True}),
    )
