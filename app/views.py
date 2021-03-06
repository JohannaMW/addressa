from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.core.urlresolvers import reverse
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

def produkte(request):
    return render(request, 'products.html')

def daten(request):
    return render(request, 'country_data.html')

def preise(request):
    return render(request, 'prices.html')

def kontakt(request):
    return render(request, 'contact.html')

def demo(request):
    return render(request, 'demo.html')

def profile(request):
    subscriptions = Subscription.objects.filter(owner=request.user)
    active_subscription = Subscription.objects.filter(owner=request.user, status=2)
    inactive_subscriptions = Subscription.objects.filter(owner=request.user, status=1)
    account_contact = AccountContact.objects.filter(account_holder=request.user)
    secret_key = SecretKey.objects.filter(owner=request.user)
    website_key = WebsiteKey.objects.filter(owner=request.user)
    return render(request, 'profile.html', {
        subscriptions : 'subscriptions',
        account_contact: 'account_contact',
        active_subscription: 'active_subscription',
        inactive_subscriptions: 'inactive_subscriptions',
        secret_key: 'secret_key',
        website_key: 'website_key'
    })

def update(request, template_name="update.html"):
    if request.method == 'POST':
        form = UpdateProfile(data=request.POST, instance=request.user)
        print(request.user)
        print "blaaa"
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.instance)
            return redirect("update")
    else:
        form = UpdateProfile(instance=request.user)
    # page_title = _('Edit user names')
    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))

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

def add_contact(request):
    contacts = AccountContact.objects.filter(account_holder=request.user)
    if request.method == 'POST':
        form = AccountContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            company = form.cleaned_data['company']
            phone = form.cleaned_data['phone']
            user = request.user
            AccountContact.objects.create(first_name=first_name, last_name=last_name, email=email, company=company,
                                          phone=phone, account_holder=user)
            return redirect("add_contact")
    else:
        form = AccountContactForm()

    return render(request, "add_contact.html", {
        'form': form, 'contacts': contacts
    })


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
                         " http://78.46.57.90/register/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'johanna.weinsziehr@gmail.com',
                [email], fail_silently=False)

            return HttpResponseRedirect('/register_confirmation')
    else:
        args['form'] = ClientRegistrationForm()

    return render_to_response('registration/register.html', args, context_instance=RequestContext(request))