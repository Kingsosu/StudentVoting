from django import forms
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from students.models import Student
from voteapp.models import Passcode, Position, AspirantListStudent

class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField(max_length=225, help_text='Required. Add a valid email address')
    matric_number = forms.CharField(max_length=20, required=False)
    role = forms.ChoiceField(choices=[('student', 'Student'), ('candidate', 'Candidate')])
    passcode = forms.CharField(max_length=12, required=False)
    position = forms.ModelChoiceField(queryset=Position.objects.all().order_by('title'), required=False)

    class Meta:
        model = Account
        fields = ('email', 'username', 'matric_number', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Email {email} is already in use')
        return email
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if Account.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Username {username} is already in use')
        return username

    
    def clean_matric_number(self):
        matric_number = self.cleaned_data["matric_number"]
        if Account.objects.filter(matric_number=matric_number).exists():
            raise forms.ValidationError(f'Matric number {matric_number} is already in use')
        try:
            student = Student.objects.get(matric_number=matric_number)
        except Student.DoesNotExist:
            raise forms.ValidationError(f'Matric number {matric_number} does not exist')
        return matric_number
            
    def clean_role(self):
        role = self.cleaned_data['role']
        if role == 'candidate':
            position = self.cleaned_data.get('position')
            matric_number = self.cleaned_data.get('matric_number')
            # Check if the candidate is already registered for the selected position
            if AspirantListStudent.objects.filter(position=position).exists():
                raise forms.ValidationError('Candidate is already registered for the selected position.')
            elif AspirantListStudent.objects.filter(student__matric_number=matric_number).exists():
                raise forms.ValidationError('Candidate is already registered for a position.')
        
        elif role != 'student':
            raise forms.ValidationError('Invalid role')
        return role

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        matric_number = cleaned_data.get('matric_number')
        position = cleaned_data.get('position')
        passcode = cleaned_data.get('passcode')

        if role == 'candidate':
            
            if Student.objects.filter(matric_number=matric_number, level=400).exists():
                pass
            elif Student.objects.filter(matric_number=matric_number, level=500).exists():
                pass
            else:
                raise forms.ValidationError('Only 400 levels students and above can register')

            passcode_objs = Passcode.objects.filter(passcode=passcode, is_used=False)
            if not passcode_objs.exists():
                raise forms.ValidationError('Invalid passcode or passcode already used')
            passcode_obj = passcode_objs.first()

            try:
                with transaction.atomic():
                    # Create the candidate
                    candidate = AspirantListStudent.objects.create(
                        matric_number=matric_number,
                        position=position,
                        student=Student.objects.get(matric_number=matric_number),
                    )
                    passcode_obj.is_used = True
                    passcode_obj.user = candidate.student  # Assuming candidate.user is the user associated with the candidate
                    passcode_obj.save()
                    
            except Exception as e:
                raise forms.ValidationError(f"Error creating candidate {str(e)}")

        return cleaned_data
    

class AccountAuthenicateForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]      
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid login, please correct your credentials')
            

            
class AccountUpateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username', 'profile_image')
    

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in use')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username {username} is already in use')
    
    def save(self, commit=True):
        account = super(AccountUpateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        # account.profile_image = self.cleaned_data['profile_image']
        if commit:
            account.save()
        return account
        

    
    
    

