from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from dashboard.models import Course

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    

class CourseForm(forms.ModelForm):
    name = forms.CharField( 
        label="Title", max_length=100,min_length=2, required = True,
        widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'pop-input-feild'}),
        error_messages={ 'required': 'The name should not be empty',
                        'min_length': 'The name should not be less than 2 characters',
                        'max_length': 'The name should not exceed 100 characters',
                        }
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "login-input-feild", "maxlength": 100})
    )
  
    from_age = forms.IntegerField(
         label="From age", required=True,
         widget=forms.TextInput(),
         error_messages={'required': 'The from age should not be empty',
                         'invalid': 'invalid age'}
    )
    to_age = forms.IntegerField(
         label="To age", required=True,
         widget=forms.TextInput(),
         error_messages={'required': 'The to age should not be empty',
                         'invalid': 'invalid age'}
    )
    class Meta:
        model = Course
        fields = ['name', 'description','from_age','to_age']
    
    def clean(self):
        cleaned_data = super(CourseForm, self).clean()
        from_age = cleaned_data.get("from_age")
        to_age = cleaned_data.get("to_age")
        if from_age and to_age and to_age < from_age:
            self.add_error('to_age', 'To age should be greater than from age.')
        return cleaned_data 