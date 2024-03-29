from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, AddCustomerForm
from .models import Customer

# Create your views here.
def home(request):
    records = Customer.objects.all()

    # Check to see if loggin in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')
        else:
            messages.success(request, 'Error logging in, please try again!')
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})



def logout_user(request):
    logout(request)
    messages.success(request, "Logout successful...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration Successful')
            return redirect('home')
    
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Customer.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, 'You need to login in order to view customer details')
        return redirect('home')
    

def delete_customer(request, pk):
    if request.user.is_authenticated:
        delete_rec = Customer.objects.get(id=pk)
        delete_rec.delete()
        messages.success(request, 'Record Deleted')
        return redirect('home')
    else:
        messages.success(request, 'You need to login in order to delete')
        return redirect('home')
    
def add_customer(request):
    form = AddCustomerForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_customer = form.save()
                messages.success(request, "Customer Added Successfully")
                return redirect('home')
        
        return render(request, 'add_record.html', {'form':form})
    else:
         messages.success(request, "You must be logged in to add customer")
         return redirect('home')

def update_customer(request, pk):
    if request.user.is_authenticated:
        current_record = Customer.objects.get(id=pk)
        form = AddCustomerForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer Updated Successfully")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to update customer")
        return redirect('home')