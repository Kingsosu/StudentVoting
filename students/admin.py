from django.contrib import admin
from students.models import Department, Faculty, Student
from django import forms


# Register your models here.
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['faculty_code', 'faculty_name']
    list_filter = ['faculty_code', 'faculty_name']
    
    class Meta:
        model = Faculty


class DepartmentAdminForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        department_code = cleaned_data.get('department_code')
        faculty = cleaned_data.get('faculty')

        if Department.objects.filter(faculty=faculty, department_code=department_code).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A department with this code already exists for this faculty.")

        return cleaned_data

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_code', 'department_name', 'faculty']
    list_filter = ['department_code', 'department_name']
    
    form = DepartmentAdminForm
    
    def faculty(self, obj):
        return obj.faculty_name
    
    class Meta:
        model = Department


class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        faculty = cleaned_data.get('faculty')

        if department and faculty and department.faculty != faculty:
            raise forms.ValidationError("Selected department does not belong to the specified faculty")

        return cleaned_data

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ['matric_number']
    list_display = ['matric_number', 'fullname', 'gender', 'level', 'department', 'faculty']
    list_filter = ['matric_number', 'level', 'department', 'fullname']
    search_fields = ['matric_number__icontains', 'fullname__icontains', 'email__icontains']
    form = StudentAdminForm
    
    class Meta:
        model = Student
        

