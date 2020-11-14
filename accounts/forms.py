from django.contrib.auth.models import User
from django import forms



class UserRegistrationForm(forms.ModelForm):

	error_css_class = "error"
	
	password1 = forms.CharField(max_length=20 , widget=forms.PasswordInput , label='Password')
	password2 = forms.CharField(max_length=20 , widget=forms.PasswordInput , label='Repeat password')

	class Meta:

		model = User
		fields = ['username']


	def clean_password2(self):

		cd = self.cleaned_data

		if cd['password1'] != cd['password2']:

			raise forms.ValidationError('Passwords do not match.')

		return cd['password2']