from django.conf import settings
from django.core import files
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Account
from accounts.forms import AccountUpateForm
from students.models import Student
from voteapp.models import AspirantListStudent, Position
from voteapp.utils import election_view, check_voting_status, get_positions_with_candidates, save_temp_profile_image_from_base64String, TEMP_PROFILE_IMAGE_NAME

import json, os, cv2, base64

# Create your views here.


# Index page
def index(request):

    context = {}
    context = election_view(request)

    return render(request, 'index.html', context)

@login_required(login_url='login')
def dashboard(request, *args, **kwargs):
    context = {}

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    username = kwargs.get('user_username')
    
    account = get_object_or_404(Account, username=username)
    
    if account != request.user:
        return HttpResponse('You are not the authenticated user')
    
    if request.user.is_staff:
        # Redirect the user to admin login
        return redirect('admin:index')

    context = election_view(request)
    
    if account:
        context['matric_number'] = account.matric_number
        context['profile_image'] = account.profile_image.url

        student = Student.objects.get(user=request.user)
        context['fullname'] = student.fullname
        context['department'] = student.department

        context['is_student'] = request.user.is_student
        context['is_candidate'] = request.user.is_candidate

        if request.user.is_candidate:
            aspirant = AspirantListStudent.objects.get(user=account)
            if aspirant:
                context['position'] = aspirant.position.title
                context['total_number_of_voter'] = aspirant.total_vote

    return render(request, 'dashboard.html', context)


# Vote page
@login_required(login_url='login')
def vote_view(request, *args, **kwargs):
    context = {}
  
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    username = kwargs.get('user_username')
    
    account = get_object_or_404(Account, username=username)
    
    if account != request.user:
        return HttpResponse('You are not the authenticated user')
    
    if request.user.is_staff:
        # Redirect the user to admin login
        return redirect('admin:index')
    
    context = election_view(request)

    # Retrieve all positions with their candidates
    positions_with_candidates = get_positions_with_candidates()

    context['positions_with_candidates'] = positions_with_candidates
    voting_status = check_voting_status(request.user.id)
    context['voting_status'] = voting_status
   
    return render(request, 'voteapp/vote.html', context)


# Submit the vote using ajax
@require_POST
def submit_vote(request):
    # get the selected candidates from the form data
    selected_candidates_json = request.POST.get('selected_candidates')
    
    if selected_candidates_json:
        try:
            # Deserialize the JSON data to python dictionary
            selected_candidates = json.loads(selected_candidates_json)

            # Process the selected candidates    
            for position_slug, candidate_id in selected_candidates.items():
                # Retrieve the selected candidate
                aspirant = AspirantListStudent.objects.get(pk=candidate_id)

                # Increment the vote count for the selected candidate
                aspirant.total_vote += 1
                aspirant.student_voters.add(request.user)
                aspirant.save()

                position_item = aspirant.position
                position_item.total_vote += 1
                position_item.voters.add(request.user)
                position_item.save()
                # user_voted('voted')
                print('voted')
            success = True
            message = 'Vote submitted successfully'
        except Exception as e:
            success = False
            message = f'Error submitting votes: {str(e)}'
    else:
        success = False
        message = 'No selected candidates found in the request'
            
    return JsonResponse({'success': success, 'message': message})


# Result page
@login_required(login_url='login')
def result_view(request, *args, **kwargs):

    context = {}

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    username = kwargs.get('user_username')
    
    account = get_object_or_404(Account, username=username)
    
    if account != request.user:
        return HttpResponse('You are not the authenticated user')
    
    if request.user.is_staff:
        # Redirect the user to admin login
        return redirect('admin:index')
    
    context = election_view(request)
        
    positions_with_results = []
    
    # Retrieve all positions
    positions = Position.objects.all().order_by('asociate_number')
        
    # Iterate over each position
    for position in positions:
        # Get all candidates for the current position
        candidates = AspirantListStudent.objects.filter(position=position)

        # Calculate total votes for the position
        total_votes = sum(candidate.total_vote for candidate in candidates)

        # Append the position and its total vote to the list
        positions_with_results.append({'position': position, 'total_votes': total_votes})
        context['positions_with_results'] = positions_with_results

        # DEBUG: Print the voting status of the logged-in user
    print("User's voting status:", check_voting_status(request.user.id))
    
    return render(request, 'voteapp/result.html', context)


# Winners page
@login_required(login_url='login')
def winners_view(request, *args, **kwargs):
    
    context = {}

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    username = kwargs.get('user_username')
    
    account = get_object_or_404(Account, username=username)
    
    if account != request.user:
        return HttpResponse('You are not the authenticated user')
    
    if request.user.is_staff:
        # Redirect the user to admin login
        return redirect('admin:index')
    
    context = election_view(request)

    winning_candidates = []

    # Get the candidate with the highest number of votes
    positions = Position.objects.all().order_by('asociate_number')
    
    for position in positions:
        
        # Get the candidate with the highest votes for the current position
        winning_candidate = AspirantListStudent.objects.filter(position=position).order_by('-total_vote').first()
        if winning_candidate:
            winning_candidates.append(winning_candidate)
        # Retrieve the candidates associated with the winning position
    context['winning_candidates'] = winning_candidates

    return render(request, 'voteapp/winners.html', context)

# Profile page
@login_required(login_url='login')
def profile_view(request, *args, **kwargs):
    
    context = {}

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    username = kwargs.get('user_username')
    
    account = get_object_or_404(Account, username=username)
    
    if account != request.user:
        return HttpResponse('You are not the authenticated user')
    
    if request.user.is_staff:
        # Redirect the user to admin login
        return redirect('admin:index')
    
    context = election_view(request)
    
    return render(request, 'voteapp/profile.html', context)


# Edit profile
@login_required(login_url='login')
def edit_profile_view(request, *args, **kwargs):
    
    context = {}

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    username = kwargs.get('user_username')
    
    account = get_object_or_404(Account, username=username)
    
    if account != request.user:
        return HttpResponse('You are not the authenticated user')
    
    if request.user.is_staff:
        # Redirect the user to admin login
        return redirect('admin:index')
    
    context = election_view(request)
    
    
    if request.POST:
        form = AccountUpateForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            # account.profile_image.delete()
            form.save()
            # messages.success(request, f"Hi {request.user.username}, your account profile has been updated successfully")
            return redirect("profile", user_username = account.username)
        else:
            form = AccountUpateForm(request.POST, initial={
                 'id' : account.id ,
                 'email' : account.email ,
                 'username' : account.username ,
                 'profile_image' : account.profile_image,
            })
            context['form'] = form
    else:
        form = AccountUpateForm(initial={
            'id' : account.id ,
            'email' : account.email ,
            'username' : account.username ,
            'profile_image' : account.profile_image,
        })
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE

    

    return render(request, 'voteapp/edit_profile.html', context)

# Saving crop image
def crop_image_view(request, *args, **kwargs):
    payload = {}
    user = request.user

    if request.POST and user.is_authenticated:
        try:
            imageString = request.POST.get('image')
            url = save_temp_profile_image_from_base64String(imageString, user)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get('cropX'))))
            cropY = int(float(str(request.POST.get('cropY'))))
            cropWidth = int(float(str(request.POST.get('cropWidth'))))
            cropHeight = int(float(str(request.POST.get('cropHeight'))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            crop_img = img[cropY:cropY + cropHeight, cropX: cropX + cropWidth]
            cv2.imwrite(url, crop_img)

            # i don't want to delete the image if file is 'kscode/profile_image.png'
            # if user.profile_image.path == 'kscode/profile_image.png':
            #     pass
            # else:
            #     user.profile_image.delete()

            if 'profile_image.png' not in user.profile_image.name:
                print('deleted')
                user.profile_image.delete()

            # Save the crop image directly to the profile_image field
            user.profile_image.save(f'profile_image_{user.username}.png', files.File(open(url, 'rb')))
            user.save()
            payload['result'] = 'success'
            payload['cropped_profile_image'] = user.profile_image.url

            os.remove(url)

        except Exception as e:
            payload['result'] = 'error'
            payload['exception'] = str(e)

    return HttpResponse(json.dumps(payload), content_type='application/json')