from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import *
from models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone


def home(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

def register_confirmation(request):
    return render(request, 'registration/confirm.html')

def confirm_expired(request):
    return render(request, 'registration/confirm_expired.html')

def register_confirm_mail(request):
    return render(request, 'registration/register_confirmation.html')

def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/home')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(Client, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('registration/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    print user_profile.is_active
    user_profile.is_active = True
    user_profile.save()
    return redirect("/register_success/")

def register(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user by username
            user=Client.objects.get(username=username)

            # Update user profile
            user.activation_key = activation_key
            user.key_expires = key_expires
            user.save()

            # Send email with activation key
            email_subject = 'Ihre Registrierung bei ADDRESSA!'
            email_body = "Hallo %s! Nur noch ein Schritt bis zur Erstellung Deines Accounts! Bitte klicke den folgenden Link innerhalb" \
                         " der naechsten 48h um die Registrierung abzuschliessen!" \
                         " http://127.0.0.1:8000/register/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'johanna.weinsziehr@gmail.com',
                [email], fail_silently=False)

            return HttpResponseRedirect('/register_confirmation')
    else:
        args['form'] = ClientRegistrationForm()

    return render_to_response('registration/register.html', args, context_instance=RequestContext(request))