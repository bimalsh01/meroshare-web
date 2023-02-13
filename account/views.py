from http.client import HTTPResponse
from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User
from utils.func import *
from account.models import History, Meroshare
from .forms import MeroshareForm, UserForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method == 'POST':
        uname = request.POST['username']
        passwd = request.POST['password']

        user = auth.authenticate(username=uname, password=passwd)

        if user is not None:
            if not user.is_staff:
                auth.login(request, user)
                messages.success(request, "You are logged in!")
                return redirect("/")
            else:
                messages.add_message(request, messages.ERROR,
                                     "You are not allowed to login!")
                return redirect("/login")

        else:
            messages.add_message(request, messages.ERROR,
                                 "Invalid Username and Password!")
            return redirect("/login")

    else:
        return render(request, 'login.html')


def register(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account Created!, You can enjoy the features!")
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR,
                                 "User Registration Failed!")
    context = {
        'form': form,
    }
    return render(request, "register.html", context)


def logout_user(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def dashboard(request):

    account_count = Meroshare.objects.all().count()
    if request.user.is_authenticated:
        user = request.user
        meroshare = Meroshare.objects.filter(linked_to=user)
        context = {
            'meroshare': meroshare,
            'account_count': account_count,
        }

    form = MeroshareForm()
    if request.method == 'POST':
        try:
            form = MeroshareForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.linked_to = request.user
                instance.save()
                messages.success(request, "Meroshare ID added successfully!")
                return redirect('/')
        except:
            messages.add_message(request, messages.ERROR,
                                 "Meroshare creationx failed!")
            return render(request, 'dashboard.html')

    return render(request, 'dashboard.html', context)


def apply(request, meroshare_id):
    meroshare = Meroshare.objects.get(id=meroshare_id)
    name = meroshare.name
    crn = meroshare.crn
    txn_pin = meroshare.pin
    dp_id = meroshare.dp
    username = meroshare.uname
    password = meroshare.pword

    if request.method == 'POST':
        print("POSTx")
        share = request.POST['company']
        kitta = request.POST['kitta']
        try:
            ipo_selector(share)
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                    "IPO Selection Failed!")
        sleep(1)
        apply_ipo(kitta,crn,txn_pin)
        history = History()
        history.appliedby_name = name
        history.applied_company = request.POST['cname']
        history.linked_to = request.user
        history.save()
        redirect('/')
        messages.success(request, "IPO Applied Successfully!")
        
    try:
        while web_driver.driver.current_url != "https://meroshare.cdsc.com.np/#/dashboard":
            meroshare_login(dp_id, username, password)
            sleep(2)

            if web_driver.driver.current_url == "https://meroshare.cdsc.com.np/#/dashboard":
                goto_asba()
                data = open_ipo_lister()
                
                # loop through the data and get the company name and company option
                ipo_list = []
                for i in data:
                    ipo_list.append(i)
                context = {
                    'name': name,
                    'ipo_list': ipo_list,
                }
                return render(request, 'apply.html', context)
            
            else:
                messages.add_message(request, messages.ERROR,
                                    "Meroshare Login Failed!")
                return redirect('/')
                

    except:
        messages.add_message(request, messages.ERROR,
                                    "Meroshare Login Failed!")
        return redirect('/')
    
@login_required(login_url='/login')
def history(request):
    history = History.objects.filter(linked_to=request.user)
    context = {
            'history': history,
        }
    return render(request, 'history.html', context)

def delete(request, meroshare_id):
    meroshare = Meroshare.objects.get(id=meroshare_id)
    meroshare.delete()
    messages.success(request, "Meroshare ID deleted successfully!")
    return redirect('/')


    

