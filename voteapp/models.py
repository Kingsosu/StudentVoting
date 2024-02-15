from django.db import models
import uuid, random, string
from students.models import Student
from django.conf import settings

class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=40, unique=True, blank=False, null=False)
    slug = models.SlugField(blank=True, null=True)
    total_vote = models.IntegerField(default=0)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    asociate_number = models.CharField(max_length=3, blank=True, null=True, default="--")

    def __str__(self):
        return self.title
     
class AspirantListStudent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    matric_number = models.CharField(max_length=40, blank=False, null=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='aspirant', null=True, blank=True, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='aspirant_student')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="aspirant_position")
    total_vote = models.IntegerField(default=0)
    student_voters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    @property
    def percentage_vote(self):
        position_vote = self.position.total_vote
        item_votes = self.total_vote

        if (position_vote == 0):
            vote_in_percentage = 0
        else:
            vote_in_percentage = (item_votes/position_vote) * 100
        
        return vote_in_percentage
    
    def __str__(self):
        return self.student.fullname 

class Passcode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    passcode = models.CharField(max_length=12, unique=True)
    is_used = models.BooleanField(default=False)
    user = models.OneToOneField(Student, blank=True, null=True, on_delete=models.SET_NULL, related_name="passcode_user")
    
    # def generate_passcode(self):
    #     characters = string.ascii_uppercase + string.digits
    #     passcode = ''.join(random.choice(characters) for _ in range(12))
    #     return passcode
    
    # def save(self, *args, **kwargs):
    #     self.passcode = self.generate_passcode()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.passcode
 
class ElectionTime(models.Model):
    election_datetime = models.DateTimeField()
    duration = models.IntegerField()

    def __str__(self):
        return (f'Election on {self.election_datetime}')
