from django.shortcuts import render, redirect
import datetime
import time

import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Profile, Property, Price, Contact, AdditionalContact

import stripe
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import User, UserCredsSaver
import uuid
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
import os
from twilio.rest import Client
from .models import Complaints, Voilation
from django.views.decorators.csrf import csrf_exempt

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ''
auth_token = ''

stripe.api_key =  ''


def home(request):

    if request.user.is_authenticated:
        profile_object = Profile.objects.filter(user=request.user).first()
        if profile_object.is_pro:
            return render(request, 'profile_page.html')
        else:
            prices = Price.objects.all()
            return render(request, 'index.html', {"prices": prices})
    else:
        prices = Price.objects.all()
        return render(request, 'index.html', {"prices": prices})


def pro_home(request):
    if request.user.is_authenticated:
        profile_object = Profile.objects.filter(user=request.user).first()
        if profile_object.is_pro:
            prices = Price.objects.all()
            return render(request, 'index.html', {"profiled": True, "prices": prices})
        else:
            prices = Price.objects.all()
            return render(request, 'index.html', {"profiled": False, "prices": prices})
    else:
        prices = Price.objects.all()
        return render(request, 'index.html', {"profiled": False, "prices": prices})


def properties_page(request):
    properties = Property.objects.filter(user=request.user)

    return render(request, 'property.html', {"properties": properties})


def property_details_page(request, property_id):
    pro = Property.objects.get(id=property_id)
    complaints = pro.complaints.all()
    voilations = pro.voilations.all()
    contacts = pro.contacts.all()
    context = {
        "pro": pro,
        "complaints": complaints,
        "voilations": voilations,
        "contacts": contacts,
    }

    return render(request, 'detail_property.html', context)


def property_search_page(request):

    return render(request, 'search_property.html')


def complaints(request):
    res_complaints = Complaints.objects.filter(
        user=request.user, complaint_status='RES')
    act_complaints = Complaints.objects.filter(
        user=request.user).exclude(complaint_status='RES')
    context = {
        "res_complaints": res_complaints,
        "act_complaints": act_complaints,
    }
    return render(request, 'complaints.html', context)


def voilations(request):

    act_voilations = Voilation.objects.filter(
        user=request.user).exclude(voilation_type__icontains='DISMISSED')
    res_voilations = Voilation.objects.filter(
        user=request.user, voilation_type__icontains='DISMISSED')
    context = {
        "res_voilations": res_voilations,
        "act_voilations": act_voilations,
    }
    return render(request, 'voilations.html', context)


def princing(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile.is_pro == True:
            prices = Price.objects.all()
            context = {"profiled": profile,
                       "prices": prices}
            return render(request, 'pricing.html', context)
        else:
            prices = Price.objects.all()
            return render(request, 'pricing.html', {"prices": prices})
    else:
        prices = Price.objects.all()
        return render(request, 'pricing.html', {"prices": prices})


def already_pro(request):
    return render(request, 'pro_user.html')


def contact(request):
    return render(request, 'contact.html')


def contact_process(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email,
                               subject=subject, message=message)

    return redirect('home')


def add_property(request):
    if request.method == "POST":
        property_name = request.POST.get('property_name')
        zip = request.POST.get('zip')
        borough = request.POST.get('borough')
        block = request.POST.get('block')
        lott = request.POST.get('lott')
        street = request.POST.get('street')
        house = request.POST.get('house')
        bin_number = request.POST.get('bin_number')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name1 = request.POST.get('name1')
        email1 = request.POST.get('email1')
        phone1 = request.POST.get('phone1')
        name2 = request.POST.get('name2')
        email2 = request.POST.get('email2')
        phone2 = request.POST.get('phone2')
        additional = request.POST.get('additional')
        additional1 = request.POST.get('additional1')
        additional2 = request.POST.get('additional2')

        property = Property(user=request.user, property_name=property_name, zip=zip, borough=borough,
                            block=block, lott=lott, street=street, house=house, bin_number=bin_number,)
        property.save()

        if additional == 'already':
            AdditionalContact(user=request.user, property=property,
                              name=name, email=email, phone=phone).save()
        else:
            contact_ = AdditionalContact.objects.get(id=additional)
            if contact_:
                AdditionalContact(user=request.user, property=property,
                                  name=contact_.name, email=contact_.email, phone=contact_.phone).save()
            else:
                pass

        if additional1 == 'already':
            AdditionalContact(user=request.user, property=property,
                              name=name1, email=email1, phone=phone1).save()
        else:
            contact__ = AdditionalContact.objects.get(id=additional1)
            if contact__:
                AdditionalContact(user=request.user, property=property,
                                  name=contact__.name, email=contact__.email, phone=contact__.phone).save()
            else:
                pass

        if additional2 == 'already':
            AdditionalContact(user=request.user, property=property,
                              name=name2, email=email2, phone=phone2).save()
        else:
            contact___ = AdditionalContact.objects.get(id=additional2)
            if contact___:
                AdditionalContact(user=request.user, property=property,
                                  name=contact___.name, email=contact___.email, phone=contact___.phone).save()
            else:
                pass

        subject = 'Property was added'
        context = {
            "status": "Property with the following details Added successfully.",
            "borough": f'Borough :  {borough}',
            "property_name": f'Property Name :  {property_name}',
            "zip": zip,
            "block": f'Block :  {block}',
            "lott": f'Lot :  {lott}',
            "house": f'House :  {house}',
            "street": f'Street :  {street}',
            "bin_number": f'BIN :  #{bin_number}',
            "fname": request.user.first_name,
        }
        from_email = settings.EMAIL_HOST_USER

        templ = get_template('property_add_delete.txt')
        messageing = templ.render(context)
        emailnew = EmailMultiAlternatives(
            subject, messageing, "Property Added", [from_email, request.user.email],)

        emailnew.content_subtype = 'html'
        emailnew.send()
        try:
            client = Client(account_sid, auth_token)

            if context["property_name"] == '':
                message = client.messages.create(
                    body=f'''Property was Added
                        \n \n {context["borough"]}, {context["house"]} {context["street"]}
                        \n \n {context["block"]} {context["lott"]}
                        \n \n {context["bin_number"]}
                    ''',
                    from_='+16468133607',
                    to=request.user.phone
                )
            else:
                message = client.messages.create(
                    body=f'''Property was Added
                         \n \n {context["borough"]}, {context["house"]} {context["street"]}
                        \n \n {context["block"]} {context["lott"]}
                        \n \n {context["bin_number"]} \n \n {context["property_name"]}
                    ''',
                    from_='+16468133607',
                    to=request.user.phone
                )
            print(message.sid)
        except Exception as e:
            print(e)

    return redirect('add_property')


def edit_property_page(request, property_id):
    pro = Property.objects.get(id=property_id)
    contacts = AdditionalContact.objects.filter(property=pro)

    return render(request, 'edit_property.html', {"pro": pro, "contacts": contacts})


def edit_contact(request, contact_id):
    contact = AdditionalContact.objects.get(id=contact_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        property_id = request.POST.get('property_id')

        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.save()

    return redirect(f'/edit-property-page/{property_id}')


def edit_property(request, property_id):
    if request.method == "POST":
        property_name = request.POST.get('property_name')
        zip = request.POST.get('zip')
        borough = request.POST.get('borough')
        block = request.POST.get('block')
        lott = request.POST.get('lott')
        street = request.POST.get('street')
        house = request.POST.get('house')
        bin_number = request.POST.get('bin_number')

        property = Property.objects.get(id=property_id)
        property.property_name = property_name
        property.zip = zip
        property.borough = borough
        property.block = block
        property.lott = lott
        property.street = street
        property.house = house
        property.bin_number = bin_number

        property.save()
        subject = 'Property was Edited'
        context = {
            "status": "Property with the following details Edited successfully.",
            "borough": f'Borough :  {borough}',
            "property_name": f'Property Name :  {property_name}',
            "zip": zip,
            "block": f'Block :  {block}',
            "lott": f'Lot :  {lott}',
            "house": f'House :  {house}',
            "street": f'Street :  {street}',
            "bin_number": f'BIN :  #{bin_number}',
            "fname": request.user.first_name,
        }
        from_email = settings.EMAIL_HOST_USER

        templ = get_template('property_add_delete.txt')
        messageing = templ.render(context)
        emailnew = EmailMultiAlternatives(
            subject, messageing, "Property Edited", [from_email, request.user.email],)

        emailnew.content_subtype = 'html'
        emailnew.send()
        try:
            client = Client(account_sid, auth_token)

            if context["property_name"] == '':
                message = client.messages.create(
                    body=f'''Property was Edited
                        \n \n {context["borough"]}, {context["house"]} {context["street"]}
                        \n \n {context["block"]} {context["lott"]}
                        \n \n {context["bin_number"]}
                    ''',
                    from_='+16468133607',
                    to=request.user.phone
                )
            else:
                message = client.messages.create(
                    body=f'''Property was Edited
                         \n \n {context["borough"]}, {context["house"]} {context["street"]}
                        \n \n {context["block"]} {context["lott"]}
                        \n \n {context["bin_number"]} \n \n {context["property_name"]}
                    ''',
                    from_='+16468133607',
                    to=request.user.phone
                )

            print(message.sid)
        except Exception as e:
            print(e)

    return redirect(f'/edit-property-page/{property_id}')


def add_properties(request):
    if request.user.is_authenticated:
        # try:
        profile = Profile.objects.filter(
            user=request.user, is_pro=True).first()
        if profile:
            all_properties = Property.objects.filter(
                user=request.user)

            contact_list = AdditionalContact.objects.filter(user=request.user)

            length = len(all_properties)
            if length < profile.can_add:

                context = {

                    "profile": profile,
                    "contact_list": contact_list
                }
                return render(request, 'add-property.html', context)

            else:
                return render(request, 'property-completed.html')

        else:
            return redirect('price')
    else:
        return redirect('login')


def delete_street_property(request, pro_id):
    if Property.objects.get(id=pro_id):
        property = Property.objects.get(id=pro_id)
        subject = 'Property was Deleted'
        context = {
            "status": "Property with the following details was deleted.",
            "borough": f'Borough: {property.borough}, ',
            "property_name": f'Property Name: {property.property_name}, ',

            "zip": property.zip,
            "block": f'Block: {property.block}, ',
            "lott": f'Lot: {property.lott}, ',
            "house": f'House: {property.house}, ',
            "street": f'Street: {property.street}, ',
            "bin_number": f'BIN: #{property.bin_number}, ',
            "fname": request.user.first_name,
        }

        from_email = settings.EMAIL_HOST_USER

        templ = get_template('property_add_delete.txt')
        messageing = templ.render(context)
        emailnew = EmailMultiAlternatives(
            subject, messageing, "Property Deleted", [from_email, request.user.email],)

        emailnew.content_subtype = 'html'
        emailnew.send()
        try:
            client = Client(account_sid, auth_token)
            if context["property_name"] == '':
                message = client.messages.create(
                    body=f'''Property was Deleted
                        \n \n {context["borough"]}, {context["house"]} {context["street"]}
                        \n \n {context["block"]} {context["lott"]}
                        \n \n {context["bin_number"]}
                    ''',
                    from_='+16468133607',
                    to=request.user.phone
                )
            else:
                message = client.messages.create(
                    body=f'''Property was Deleted
                         \n \n {context["borough"]}, {context["house"]} {context["street"]}
                        \n \n {context["block"]} {context["lott"]}
                        \n \n {context["bin_number"]} \n \n {context["property_name"]}
                    ''',
                    from_='+16468133607',
                    to=request.user.phone
                )

            print(message.sid)
        except Exception as e:
            print(e)
        print(context)

        property.delete()

        return redirect('properties_page')
    return redirect('properties_page')


def payment_after_registeration(request, param1):
    user = User.objects.get(id=param1)
    price = Price.objects.all()
    context = {
        "user_id": user.id,
        "prices": price
    }

    return render(request, 'choose_package.html', context)


def payment_at_registration(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        account_type = request.POST.get('account_type')
        session = stripe.checkout.Session.create(
            line_items=[{
                'price': account_type,
                'quantity': 1
            }],

            mode='subscription',
            metadata={"user_id": user_id,
                      "price_model_token": account_type},
            success_url=request.build_absolute_uri(
                reverse('success_3')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(
                reverse('cancel'))

        )

        context = {
            'session_id': session.id
        }
        return render(request, 'checkout.html', context)

    else:
        return redirect('price')


def update_subscription(request):
    return render(request, 'update_subscrption.html')


@login_required(login_url='login')
def become_pro(request):
    if request.method == 'POST':
        user_id = request.user.id
        account_type = request.POST.get('account_type')
        session = stripe.checkout.Session.create(
            line_items=[{
                'price': account_type,
                'quantity': 1
            }],

            mode='subscription',
            metadata={"user_id": user_id,
                      "price_model_token": account_type},
            success_url=request.build_absolute_uri(
                reverse('success_2')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(
                reverse('cancel'))

        )

        context = {
            'session_id': session.id
        }
        return render(request, 'checkout.html', context)

    else:
        return redirect('price')


def calculate_price(number):
    if number == 1:
        return 1*100
    elif number < 10:
        return (10*number)*100
    elif number <= 20 and number >= 10:
        return (number*8)*100
    elif number <= 50 and number >= 21:
        return (number*6)*100
    elif number > 50:
        return (number*4)*100


def change_subscription(request):
    if request.method == 'POST':

        user_obj = request.user
        profile = Profile.objects.filter(user=user_obj).first()
        number_of_properties = int(
            request.POST.get('number')) + int(profile.can_add)
        subscription_price = calculate_price(number=number_of_properties)

        product = stripe.Product.create(
            name='Your Subscription Product',
            type='service',
            statement_descriptor='Your Subscription'
        )
        # Create a price for the new subscription product
        price = stripe.Price.create(
            product=product.id,
            unit_amount=subscription_price,  # Convert dollars to cents
            currency='usd',
            recurring={
                'interval': 'month'
            }
        )

        print("this is the price id")
        print(price.id)
        print(" this was the price id")
        # Retrieve the user's current subscription
        customer = stripe.Customer.retrieve(profile.strip_costumer_token)
        subscription = stripe.Subscription.retrieve(
            profile.strip_subscription_token)
        # Update the user's subscription to the new product
        updated_subscription = stripe.Subscription.modify(
            subscription.id,
            proration_behavior='create_prorations',
            items=[{
                'id': subscription['items']['data'][0].id,
                'price': price.id,
            }],
            metadata={"updated": "yes",
                      "user_id": user_obj.id,
                      'price_model_token': price.id,
                      "properties": number_of_properties},

            proration_date=int(time.time()),
        )
        # Charge the user the proration amount
        proration_invoice = stripe.Invoice.create(
            customer=customer.id,
            subscription=updated_subscription.id,

            auto_advance=True,
        )

        return redirect('success_2')


def success_second(request):
    return render(request, 'success2.html')


def success_third(request):
    return render(request, 'success_3.html')


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')


def twenty_plus(request):
    return render(request, 'twenty_plus.html')


def login_attempt(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()

        if user is None:
            messages.error(request, "User doesn't exist.")
            return redirect('login')

        user = authenticate(email=email, password=password)

        if user is None:

            messages.error(request, "Password Wrong!.")
            forget = True
            return render(request, 'login.html',  {"forget": forget})

        profile_obj = Profile.objects.filter(user=user).first()
        if not profile_obj.is_verified:
            messages.success(
                request, 'Email is not verified check your email inbox.')
            return redirect('login')
        else:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            company = request.POST.get('cname')
            address_first = request.POST.get('address_first')
            address_second = request.POST.get('address_second')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip = request.POST.get('zip')
            phone = request.POST.get('phone')
            fax = request.POST.get('fax')
            cell = request.POST.get('cell')
            our_source = request.POST.get('our_source')
            account_type = request.POST.get('account_type')
            username = fname+state+email

            user = User.objects.filter(email=email)
            usern = User.objects.filter(username=username)
            if user or usern:
                messages.success(
                    request, 'User already exists.')
                return redirect('register')
            else:
                messages.success(
                    request, 'User Created successfuly.')
                addresses = address_first + ' ' + address_second

                user = User(email=email, username=username, first_name=fname, last_name=lname, phone=phone, company_name=company,
                            address=addresses, city=city, state=state, zip=zip, fax=fax, cell=cell, our_source=our_source,)
                user.set_password(password)
                user.save()
                user_id = user.id
                UserCredsSaver.objects.create(
                    user=user, email=email, password=password)

                login(request, user)
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(
                    user=user, auth_token=auth_token)
                profile_obj.save()
                logout(request)

                send_mail_after_registration(
                    email=email, auth_token=auth_token, fname=fname)
                return redirect("verify_email")

    return render(request, 'register.html')


def user_prof(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    properties = Property.objects.filter(user=user)
    subscription = subscription = stripe.Subscription.retrieve(
        profile.strip_subscription_token)

    price = subscription["plan"]["amount"] / 100
    created_at = subscription["created"]
    current_period_start = subscription["current_period_start"]
    current_period_end = subscription["current_period_end"]
    # plan_name = subscription["plan"]

    created_at_date = datetime.datetime.fromtimestamp(created_at)
    current_period_start_date = datetime.datetime.fromtimestamp(
        current_period_start)
    current_period_end_date = datetime.datetime.fromtimestamp(
        current_period_end)

    delta = current_period_end_date - current_period_start_date

    created_at_date = datetime.datetime.fromtimestamp(
        created_at).strftime('%Y-%m-%d')
    current_period_start_date = datetime.datetime.fromtimestamp(
        current_period_start).strftime('%Y-%m-%d')
    current_period_end_date = datetime.datetime.fromtimestamp(
        current_period_end).strftime('%Y-%m-%d')

    number_of_days = delta.days

    calculate_life = int(number_of_days)/30 * 100
    life = 100-calculate_life

    property_consumed = int(properties.count())/int(profile.can_add)*100
    print(profile.profile_image)
    # print()
    context = {
        "user": user,
        "profile": profile,
        "properties": properties,
        "property_consumed": int(property_consumed),
        "price": price,
        "life": life,
        "created": created_at_date,
        "current_start": current_period_start_date,
        "current_end": current_period_end_date,
        "number_of_days": number_of_days
    }
    return render(request, 'user_prof.html', context)


def verify_email(request):
    return render(request, 'verifyEmail.html')


@ login_required(login_url='login')
def edit_user_information(request):
    return render(request, 'edit_user_information.html')


def change_profile_image(request):
    user = request.user
    if request.method == 'POST':
        p_image = request.FILES.get('profile_picture')
        print(f"This is the image uploaded right now {p_image} ")
        profile = Profile.objects.filter(user=user).first()

        profile.profile_image = p_image
        profile.save()
        messages.success(request, 'Profile image changed successfully!')
        return redirect('user_prof')

    else:

        return render(request, 'user_prof.html')


@ login_required(login_url='login')
def update_profile_info(request):
    user = request.user
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')

        if fname == '':
            pass
        else:
            user.first_name = fname

        if lname == '':
            pass
        else:
            user.last_name = lname

        if phone == '':
            pass
        else:
            user.phone = phone

        if email == '':
            pass
        else:
            user.email = email

        if address == '':
            pass
        else:
            user.address = address

        user.save()

        messages.success(request, 'Your account is updated!')
        return redirect('user_prof')


@ login_required(login_url='login')
def update_password_info(request):

    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            password = request.POST.get('password')
            password2 = request.POST.get('confirm_password')
            if password != password2:

                messages.warning(
                    request, "Password and confirm password do not macth")
                return redirect('edit_user_information')
            else:
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password changed! ')

                return redirect('edit_user_information')
        else:
            return redirect('edit_user_information')
    else:
        return redirect('edit_user_information')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:

            subject = 'Welcome to 311Alert'
            user = profile_obj.user
            fname = user.first_name
            usercreds = UserCredsSaver.objects.get(user=user)
            email = usercreds.email
            password = usercreds.password
            context = {
                "fname": fname,
                "password": password,
                "email": email
            }
            print(context)

            from_email = settings.EMAIL_HOST_USER

            templ = get_template('welcometemplate.txt')
            messageing = templ.render(context)
            emailnew = EmailMultiAlternatives(
                subject, messageing, "311Alert Joined Successfully", [from_email, user.email],)

            emailnew.content_subtype = 'html'
            emailnew.send()

            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                if profile_obj.is_pro:
                    return redirect('login')
                else:
                    return redirect('payment_after_registeration', param1=user.id)
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('payment_after_registeration', param1=user.id)

        else:
            messages.success(
                request, 'Invalid url try again or contact support team.')
            return redirect('login')
    except Exception as e:
        print(e)
        return redirect('home')


@csrf_exempt
def stripe_webhook(request):
    from datetime import datetime

    endpoint_secret = 'whsec_TrwGh7Oxsr4SKcKjhKqvyg1gj0IjZFMb'

    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']
    print('<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><><><')
    print(' HEader starts from here')
    print(sig_header)
    print(' Header ends here')
    print(' ---------------..............................                 .....................--------------------------------------')

    print(payload)
    print(' ---------------..............................                 .....................--------------------------------------')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        print(event)

    except ValueError as e:
        # Invalid payload
        raise e

    if event["type"] == "customer.subscription.updated":

        session = event["data"]["object"]
        if session["metadata"]["updated"] == "yes":

            subscription = session["items"]["data"][0]["subscription"]
            print(subscription)
            user = User.objects.get(id=session['metadata']['user_id'])

            properties = session['metadata']['properties']
            profile_object = Profile.objects.filter(user=user).first()

            can_add_properties = properties
            profile_object.is_pro = True
            profile_object.can_add = can_add_properties
            profile_object.strip_costumer_token = session['customer']
            profile_object.strip_subscription_token = subscription
            profile_object.pro_start_date = datetime.now()

            subject = '311Alert Payment Sucessful'

            profile_object.save()

        else:
            pass

    # handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(session['amount_subtotal'])
        print(session['amount_total'])
        print(session['customer'])
        print(session['customer_details']['email'])
        print(session['customer_details']['name'])
        print('---------------------------------------------')
        user = User.objects.get(id=session['metadata']['user_id'])
        price = Price.objects.get(
            token=session['metadata']['price_model_token'])
        profile_object = Profile.objects.filter(user=user).first()

        can_add_properties = price.number_of_properties
        profile_object.is_pro = True
        profile_object.can_add = can_add_properties
        profile_object.strip_subscription_token = session['subscription']

        profile_object.strip_costumer_token = session['customer']
        profile_object.pro_start_date = datetime.now()

        subject = '311Alert Payment Sucessful'

        if price.is_yearly == True:

            profile_object.is_yearly = True
            profile_object.save()
            sub_total_money = int(session['amount_subtotal'])/100
            total_money = int(session['amount_total'])/100
            context = {
                "fname": user.first_name,
                "subscribed": price.name,
                "pay_id": session['customer'],
                "package": "Yearly",
                "properties": price.number_of_properties,
                "biller_name": session['customer_details']['name'],
                "sub_total": sub_total_money,
                "total": total_money,

            }

            from_email = settings.EMAIL_HOST_USER

            templ = get_template('invoicetemplate.txt')
            messageing = templ.render(context)
            emailnew = EmailMultiAlternatives(
                subject, messageing, "311Alert Joined Successfully", [from_email, session['customer_details']['email']],)

            emailnew.content_subtype = 'html'
            emailnew.send()
        else:
            profile_object.is_yearly = False
            profile_object.save()
            sub_total_money = int(session['amount_subtotal'])/100
            total_money = int(session['amount_total'])/100

            context = {
                "fname": user.first_name,
                "subscribed": price.name,
                "package": "Monthly",
                "pay_id": session['customer'],

                "properties": price.number_of_properties,
                "biller_name": session['customer_details']['name'],
                "sub_total": sub_total_money,
                "total": total_money,

            }

            from_email = settings.EMAIL_HOST_USER

            templ = get_template('invoicetemplate.txt')
            messageing = templ.render(context)
            emailnew = EmailMultiAlternatives(
                subject, messageing, "311Alert Joined Successfully", [from_email, session['customer_details']['email']],)

            emailnew.content_subtype = 'html'
            emailnew.send()

    return HttpResponse(status=200)


def ChangePassword(request, auth_token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/password-reset-verification/{auth_token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/password-reset-verification/{auth_token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Password Changed Successfully.')

            return redirect('login')

    except Exception as e:
        print(e)
    return render(request, 'change_password.html', context)


def ForgetPassword(request):
    try:
        users = User.objects.all()
        print(users)
        if request.method == 'POST':
            somedata = request.POST.get('inputsomething')

            if User.objects.filter(username=somedata).first():
                user_obj = User.objects.get(username=somedata)
                profile = Profile.objects.filter(user=user_obj).first()
                auth_token = profile.auth_token
                print(profile)

                send_mail_for_password_reset(
                    email=user_obj.email, auth_token=auth_token, fname=user_obj.first_name)
                messages.success(
                    request, 'An email is sent to your registered email.')
                return redirect('forget_password')
            elif User.objects.filter(email=somedata).first():
                user_obj = User.objects.get(email=somedata)
                profile = Profile.objects.filter(user=user_obj).first()
                auth_token = profile.auth_token
                print(profile)

                send_mail_for_password_reset(
                    email=user_obj.email, auth_token=auth_token, fname=user_obj.first_name)
                messages.success(
                    request, 'An email is sent to your registered email.')
                return redirect('forget_password')
            else:
                messages.success(request, 'No user found.')
                return redirect('forget_password')

    except Exception as e:
        print(e)
    return render(request, 'forgot_password.html')


def send_mail_for_password_reset(email, auth_token, fname):
    subject = 'Your accounts need to be verified'
    link = f'https://311alert.info/password-reset-verification/{auth_token}'

    context = {
        "link": link,
        "fname": fname,
    }

    from_email = settings.EMAIL_HOST_USER

    templ = get_template('resettempletext.txt')
    messageing = templ.render(context)
    emailnew = EmailMultiAlternatives(
        subject, messageing, "Reset Password", [from_email, email],)

    emailnew.content_subtype = 'html'
    emailnew.send()


def send_mail_after_registration(email, auth_token, fname):
    subject = 'Your accounts need to be verified'
    link = f'https://311alert.info/verify/{auth_token}'

    context = {
        "link": link,
        "fname": fname,
    }

    from_email = settings.EMAIL_HOST_USER

    templ = get_template('templetext.txt')
    messageing = templ.render(context)
    emailnew = EmailMultiAlternatives(
        subject, messageing, "Verify Email", [from_email, email],)

    emailnew.content_subtype = 'html'
    emailnew.send()


def logout_attempt(request):
    logout(request)
    return redirect('/')
