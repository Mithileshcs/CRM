from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.

def home(request):

    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #for authentication of the username and password
        user = authenticate(request,username = username , password = password)

        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged In Successfully!")
            # return render(request,'home.html',{'username':username}) this line is if you want to display the username in that page
            return redirect('home')
        else:
            messages.success(request,"There was an error in Login In , try again...")
            return redirect('home')
    else:
        return render(request, 'home.html',{'records':records})


def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged Out Successfully!")
    return render(request, 'home.html',{})


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username , password=password)

            login(request,user)
            messages.success(request,"You have successfully Registered! , Welcome")
            return redirect('home')
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

    return render(request, 'register.html', {'form':form})



def customer_record(request,pk):
    if request.user.is_authenticated:
        #Look up for records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})

    else:
        messages.success(request,"You must Log In to view Records")
        return redirect('home')



def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id =pk)
        delete_it.delete()
        messages.success(request,"Record Deleted Successfully....")
        return redirect('home')
    
    else:
        messages.success(request,"You must Log In to Delete Record")
        return redirect('home')



def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request,"Record Added Successfully....")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request,"You must Log In to Add Record")
        return redirect('home')


def update_record(request,pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id =pk)
        form = AddRecordForm(request.POST or None, instance = current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record Updated Successfully....")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request,"You must Log In to Update Record")
        return redirect('home')



