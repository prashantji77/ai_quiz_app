
from django.shortcuts import render, redirect
from django.views import View
from quizapp.forms import CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

class CustomerRegistrationView(View):
 def get(self,request):
  form=CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html',{'form':form})
 
 def post(self, request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'User Registered Successfully !!')
   form.save()
  return render(request, 'app/customerregistration.html',{'form':form})
 

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')