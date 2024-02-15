# generatepasscode.py
from django.core.management.base import BaseCommand
from voteapp.models import Passcode
import random, string

class Command(BaseCommand):
    help = 'Generate passcode for candidate'

    def generate_passcode(self):
        characters = string.ascii_uppercase + string.digits
        passcode = ''.join(random.choice(characters) for _ in range(12))
        return passcode

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Indicates the number of candidate passcodes to be created')

    def handle(self, *args, **kwargs):
        count = kwargs['count']

        for _ in range(count):
            try:
                passcode = Passcode.objects.create(passcode=self.generate_passcode())
                passcode.save()
                self.stdout.write(self.style.SUCCESS(f'Passcode "{passcode.passcode}" created'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error creating passcode: {e}'))
                print(f'Debug info: {passcode.__dict__}')  # Add this line for debug information
