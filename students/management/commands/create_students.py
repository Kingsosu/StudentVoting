from datetime import datetime
from django import forms
from django.core.management.base import BaseCommand
from students.models import Student, Faculty, Department
from faker import Faker
import random
import time

fake = Faker()

class Command(BaseCommand):
    help = 'Create fake student records'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Indicates the number of students to be created')

    def handle(self, *args, **kwargs):
        count = kwargs['count']

        year_levels = {
            2024: '500',
            2020: '400',
            2021: '300',
            2023: '200',
            2024: '100',
        }

        gender_choices = ('M', 'F')
        religion_choices = ('CHRISTIANITY', 'ISLAM', 'OTHER')
        email_servers = ['gmail.com', 'yahoo.com', 'outlook.com']  # Add your desired email servers

        faculties = Faculty.objects.all()
        engineering_faculty = Faculty.objects.get(faculty_code='03')  # Assuming 'EN' is the faculty_code for Engineering
        departments = Department.objects.all()

        for _ in range(count):
            
            faculty = random.choice(faculties)
            department = random.choice(departments.filter(faculty=faculty))
            admission_year = random.choice(list(year_levels.keys()))
            religion=random.choice(religion_choices)
            gender=random.choice(gender_choices)
            level = year_levels[admission_year]

            try:

                full_name = fake.name()
                email_server = random.choice(email_servers)
                email = f"{full_name.replace(' ', '.').lower()}@{email_server}"
                
                student = Student(
                    fullname=full_name,
                    religion=religion,
                    gender=gender,
                    level=level,
                    faculty=faculty,
                    department=department,
                    year_of_admission=datetime.strptime(f'{admission_year}-01-01', '%Y-%m-%d').date(),
                    email=email,
                )

                student.save()

                self.stdout.write(self.style.SUCCESS(f'Student "{student.fullname}" created'))

            except forms.ValidationError as e:
                self.stderr.write(self.style.ERROR(f'Error creating student: {e}'))

            end_time = time.time()
