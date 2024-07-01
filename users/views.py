from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from users.models import Profile
from users.models import Requests
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from users.forms import profileUpdateForm, userUpdateForm


@login_required
def profile(request):
    """
    View for handling user profile updates.

    - Displays user profile form.
    - Updates user information and profile picture if form data is valid.
    - Redirects to the profile page with success message after update.
    """
    if request.method == 'POST':
        u_form = userUpdateForm(request.POST, instance=request.user)
        p_form = profileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated successfully!')
            return redirect('users:profile')
    else:
        u_form = userUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile/profile.html', context)

def request_account(request):
    """
    View for handling teacher account requests.

    - Saves user request details to Requests model.
    - Updates user profile to indicate teacher status.
    - Sends notification emails to user and admin.
    - Redirects to the home page with an info message after successful request submission.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        profile = request.user.profile
        request_instance = Requests(profile=profile, name=name, email=email, phone_number=phone_number)
        request_instance.save()
        profile_id = profile.id
        Profile.objects.filter(id=profile_id).update(is_teacher=True)
        
        message = 'Your request for a teacher account has been accepted! Now you can go back to LearnOnline and upload courses and lessons. Good luck!'
        send_mail(
            'LearnOnline, your request was accepted.',
            message,
            'learnonline@no-reply.com',
            [email],
            fail_silently=False,
        )
        send_mail(
            'LearnOnline',
            'Someone requested a teacher account. Info: ' + name + ' , ' + email + ' , ' + phone_number + ' , ' + str(profile) + '.',
            'learnonline@no-reply.com',
            ['rumelnhors52@gmail.com'],
            fail_silently=False,
        )
        messages.info(request, 'Your request was successfully sent. You will be notified by email.')
        return redirect('courses:home')
    

