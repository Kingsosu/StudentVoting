from django.shortcuts import render, redirect
from voteapp.models import Position
from accounts.forms import RegistrationForm, AccountAuthenicateForm
from accounts.models import Account
from students.models import Student
from voteapp.models import AspirantListStudent
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def registration_view(request):
    context = {}
    positions = Position.objects.all().order_by('asociate_number')
    context['position'] = positions

    user = request.user

    if user.is_authenticated:
        return redirect('dashboard', user_username=request.user.username)

    form = RegistrationForm()

    if request.method == 'POST' and request.is_ajax():
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = form.cleaned_data['role'] == 'student'
            user.is_candidate = form.cleaned_data['role'] == 'candidate'
            matric_number = form.cleaned_data.get('matric_number')
            user.save()

            if user.is_candidate:
                try:
                    aspirant = AspirantListStudent.objects.get(matric_number=matric_number)
                    if aspirant:
                        aspirant.user = user
                        aspirant.save()
                        print('successfully added the user')
                except AspirantListStudent.DoesNotExist:
                    print('error')
                    print(str(e))

            try:
                student = Student.objects.get(matric_number=matric_number)
                if student:
                    student.user = user
                    student.save()
            except Exception as e:
                print('error')
                print(str(e))
                return JsonResponse({'success': False, 'message': f'{str(e)}' })
            print('account created successfuly')
            return JsonResponse({'success': True, 'message': 'Registration successful', 'user_username': user.username})
        else:
            errors = form.errors
            non_field_errors = form.non_field_errors()
            # errors = dict(form.errors.items())
            return JsonResponse({'success': False, 'errors': errors, 'non_field_errors': non_field_errors, 'message': 'Registration failed. Please correct the errors.'})
    else:
        context['form'] = RegistrationForm()
        
    return render(request, 'accounts/register.html', context)

def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect('dashboard', user_username=request.user.username)
    
    form = AccountAuthenicateForm()

    if request.method == 'POST' and request.is_ajax():
        form = AccountAuthenicateForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                next_url = request.POST.get('next')
                if next_url:
                    return JsonResponse({'success': True, 'message': 'Login successful', 'user_username': user.username, 'next': next_url})
                else:
                    return JsonResponse({'success': True, 'message': 'Login successful', 'user_username': user.username})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid email or password'})
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'message': 'Invalid form submission', 'errors': errors})
    else:
        context['form'] = AccountAuthenicateForm()
    return render(request, 'accounts/login.html', context)


# def login_view(request):
#     context = {}
#     user = request.user
#     msg = ""
   
#     if user.is_authenticated:
#         return redirect('dashboard', user_username = request.user.username)
    
#     form = AccountAuthenicateForm()
    
#     if request.POST:
#         form = AccountAuthenicateForm(request.POST)
#         if form.is_valid():
#             email = request.POST.get('email')
#             password = request.POST.get('password')

#             user = authenticate(email=email, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 if "next" in request.POST:
#                     return redirect(request.POST.get("next"))
#                 else:
#                     return redirect("dashboard", user_username=request.user.username)
#             else:
#                 msg = 'Invalid email or password.'  # Corrected assignment of the message
#             context['msg'] = msg
#     context['form'] = form

#     return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect("index")
