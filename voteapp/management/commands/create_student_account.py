from datetime import datetime
from django.core.management.base import BaseCommand
from students.models import Student
from accounts.models import Account
import random
import time

class Command(BaseCommand):
    help = 'Create fake student account'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='Indicates the number of students account to be created')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        students = list(Student.objects.all())

        for _ in range(count):
            student = random.choice(students)

            # Generate account username from email
            email_parts = student.email.split('@')
            username_choices = [f'{email_parts[0]}11', f"{email_parts[0]}12", f"{email_parts[0]}76", email_parts[0]]
            username = random.choice(username_choices)     
            
            try:
                # Generate account
                account = Account.objects.create(
                    username=username,
                    email=student.email,
                    matric_number=student.matric_number,
                    is_student=True
                )
                account.set_password('general123')
                account.save()
                student.user = account
                student.save()
                self.stdout.write(self.style.SUCCESS(f"Account created for student {student.fullname} created"))
            except Exception as e:
                    print(e)
                    continue  # Skip the current iteration if account creation fails
            
            self.stdout.write(self.style.SUCCESS("All accounts student lists created successfully'"))