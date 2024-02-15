import random
import uuid

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django import forms
from django.db import IntegrityError


class Faculty(models.Model):
    faculty_code = models.CharField(max_length=2, unique=True)
    faculty_name = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.faculty_code:
            last_faculty = Faculty.objects.order_by('-faculty_code').first()
            if last_faculty:
                self.faculty_code = f"{int(last_faculty.faculty_code) + 1:02d}"
            else:
                self.faculty_code = "01"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.faculty_code}] - {self.faculty_name}"
   
class Department(models.Model):
    department_code = models.CharField(max_length=2)
    department_name = models.CharField(max_length=50, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.department_code:
            last_department = Department.objects.filter(faculty=self.faculty).order_by('-department_code').first()
            if last_department:
                self.department_code = f"{int(last_department.department_code) + 1:02d}"
            else:
                self.department_code = "01"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.department_name}"


class Student(models.Model):
    LEVEL_CHOICES = [
        ('100', '100 Level'),
        ('200', '200 Level'),
        ('300', '300 Level'),
        ('400', '400 Level'),
        ('500', '500 Level'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    RELIGION_CHOICES = [
        ("CHRISTIANITY", 'Christianity'),
        ("ISLAM", 'Islam'),
        ("OTHER", 'Other'),
    ]
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)
    gender = models.CharField(max_length=10, blank=False, null=False, choices=GENDER_CHOICES)

    student_id = models.CharField(max_length=3, db_index=True, editable=False)
    matric_number = models.CharField(max_length=20, unique=True, editable=False)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year_of_admission = models.DateField()
    
    profile = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)    
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.student_id:
            department_code = self.department.department_code if self.department else '000'
            last_student = Student.objects.filter(department=self.department, level=self.level).order_by('-id').first()
            
            if last_student:
                last_id = int(last_student.student_id[-3:])
                new_id = last_id + 1
            else:
                new_id = 1
            
            self.student_id = f"{new_id:03d}"

            while Student.objects.filter(department=self.department, level=self.level, student_id=self.student_id).exists():
                new_id += 1
                self.student_id = f"{new_id:03d}"
        
        if self.year_of_admission:
            self.year_of_admission = self.year_of_admission.replace(day=1, month=1)
            last_two_digits = str(self.year_of_admission.year)[-2:]

        else:
            last_two_digits = "00"

        # if self.department.faculty != self.faculty:
        #     raise forms.ValidationError('Selected department does not belong to the specified faculty')
        def clean(self):
            if self.department.faculty != self.faculty:
                raise ValidationError('Selected department does not belong to the specified faculty')
        
        self.faculty_code = self.faculty.faculty_code
        self.department_code = self.department.department_code

        self.matric_number = f"{last_two_digits}/{int(self.faculty_code):02d}/{int(self.department_code):02d}/{self.student_id}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname


