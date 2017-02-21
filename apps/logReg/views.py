from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
# Create your views here.
def index(request):
    if 'id' in request.session:
        return redirect('/success')
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'logReg/index.html', context)
def process(request):
    if request.method == 'POST':
        user_check = User.objects.reg(request.POST['first'], request.POST['last'], request.POST['email'], request.POST['password'], request.POST['confirm'])
        if user_check == False:
            messages.add_message(request, messages.INFO, 'Registration failed')
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Registration is successful')
            return redirect('/success')
def log_in(request):
    if User.objects.log(request.POST['elog'], request.POST['plog']) == False:
        messages.add_message(request, messages.INFO, 'Log in failed')
        return redirect('/')
    else:
        if 'id' not in request.session:
            request.session['id'] = User.objects.log(request.POST['elog'], request.POST['plog'])
            messages.add_message(request, messages.INFO, 'Log in successful')
            return redirect('/success')
def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'users': User.objects.get(id=request.session['id'])
        }
        return render(request, 'logReg/success.html', context)
def log_out(request):
    del request.session['id']
    return redirect('/')