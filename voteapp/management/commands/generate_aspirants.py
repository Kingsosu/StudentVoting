import random
from django.core.management.base import BaseCommand
from students.models import Student
from accounts.models import Account
from voteapp.models import AspirantListStudent, Position

class Command(BaseCommand):
    help = 'Generate accounts and aspirant student lists for 400 levels students'
    
    # def add_arguments(self, parser):
        # parser.add_argument('count_per_position', type=int, help='Number of aspirants to generate for each position')
    def add_arguments(self, parser):
        parser.add_argument('--count_per_position', type=int, help='Indicates the number of candidate passcodes to be created')

    def handle(self, *args, **kwargs):
        count_per_position = kwargs['count_per_position']
        positions = Position.objects.all()

        # Get all 400 level students and shuffle them
        students = list(Student.objects.filter(level=400))
        random.shuffle(students)

        # Iterate over each position
        for position in positions:
            students_for_position = students[:count_per_position]

            # Iterate over the first five students for this position
            for student in students_for_position:
                # Generate account username from email
                email_parts = student.email.split('@')
                username_choice = [email_parts[0] + '11' , email_parts[0] + '12', email_parts[0] + '76', email_parts[0] + '']
                username = random.choice(username_choice)

                try:
                    # Generate account
                    account = Account.objects.create(
                        username=username,
                        email=student.email,
                        matric_number=student.matric_number,
                    )
                    account.set_password('general123')
                    account.is_candidate = True
                    account.save()
                except Exception as e:
                    print(e)
                    continue  # Skip the current iteration if account creation fails

                # Generate aspirant student list
                aspirant = AspirantListStudent.objects.create(
                    student=student,
                    user=account,
                    position=position,
                    matric_number=student.matric_number
                )

                stu = Student.objects.get(matric_number=student.matric_number)
                stu.user = account
                stu.save()


                # Save the aspirant student list
                aspirant.save()

                self.stdout.write(self.style.SUCCESS(f'Account and aspirant student list created for {student.matric_number}'))

            # Remove the processed students from the list
            students = students[count_per_position:]

        self.stdout.write(self.style.SUCCESS('All accounts and aspirant student lists created successfully'))
