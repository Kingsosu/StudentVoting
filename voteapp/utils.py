from django.utils import timezone
from voteapp.models import ElectionTime, AspirantListStudent, Position

from datetime import timedelta


# Check if user has voted
def check_voting_status(user_id):
    aspirants = AspirantListStudent.objects.all()
    for aspirant in aspirants:
        if aspirant.student_voters.filter(id=user_id).exists():
            # print(aspirant)
            return True
    # print('False')
    return False

# Election logic
def election_view(request):

    context = {}

    # Get the current time in the server's timezone
    current_time = timezone.now()

    # Fetch election time
    election_time = ElectionTime.objects.first()

    if election_time:
        context['election_time'] = election_time
        
        if current_time < election_time.election_datetime:
            # Election has not started yet
            context['election_status'] = 'not_started'
            context['countdown_to_start'] = election_time.election_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        elif current_time < election_time.election_datetime + timedelta(hours=election_time.duration):
            # Election is ongoing
            context['election_status'] = 'ongoing'
            # Calculate the end time by adding the duration to election datetime
            election_end_time = election_time.election_datetime + timedelta(hours=election_time.duration)
            # Format the end time as string
            context['countdown_to_end'] = election_end_time.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            # Election has ended
            context['election_status'] = 'ended'
    else:
        context['election_status'] = 'no_schedule'

    return context


# Get position with candidates
def get_positions_with_candidates():
    
    """
    Retrieve all positions with their associated candidates.
    """
    positions = Position.objects.all().order_by('asociate_number')
    positions_with_candidates = []

    #Iterate over each position
    for position in positions:
        # Check if there are candidates for the current position
        candidates_exist = AspirantListStudent.objects.filter(position=position).exists()

        # if candidates exist, append the position and candidates to the list
        if candidates_exist:
            candidates = AspirantListStudent.objects.filter(position=position)
            positions_with_candidates.append({'position': position, 'candidates': candidates})

    return positions_with_candidates


# croping image and save it temp folder
# Cropimage image
import os, base64
from django.conf import settings
from django.core import files
from django.core.files.storage import FileSystemStorage, default_storage


TEMP_PROFILE_IMAGE_NAME = 'temp_profile_image.png'

def save_temp_profile_image_from_base64String(imageString, user):
    INCORRECT_PADDING_EXCEPTION = 'incorrect padding'
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(f'{settings.TEMP}/{str(user.pk)}'):
            os.mkdir(f'{settings.TEMP}/{str(user.pk)}')
        url = os.path.join(f'{settings.TEMP}/{str(user.pk)}', TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
             destination.write(image)
             destination.close()
        return url
    except Exception as e:
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += '=' * ((4-len(imageString) % 4 ) % 4)
            return save_temp_profile_image_from_base64String(imageString, user)
        
    return None