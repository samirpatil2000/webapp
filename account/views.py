from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm#, AccountUpdateForm

# Create your views here.
def index(request):
    return render(request,'account/home.html')


def registration_view(request):
    redirect_to=request.GET.get('next','')

    context = {}

    if redirect_to != "" or redirect_to is not None:
        context['redirect_to'] = redirect_to

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            if redirect_to== "" or redirect_to is None:
                return redirect('index')
            return HttpResponseRedirect(redirect_to)
        else:
            context['registration_form'] = form

    else: #GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')



def login_view(request):
    # redirect_to = request.GET['next']
    redirect_to = request.GET.get('next','')
    context={}
    # print(redirect_to)

    user=request.user
    if user.is_authenticated:
        return redirect('index')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                # print(HttpResponseRedirect(redirect_to_2))
                if redirect_to == "" or redirect_to is None:
                    return redirect('index')
                return HttpResponseRedirect(redirect_to)
                # return redirect('index')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    if redirect_to != "" or redirect_to is not None:
        context['redirect_to'] = redirect_to

    # print(form)
    return render(request, "account/login.html", context)


