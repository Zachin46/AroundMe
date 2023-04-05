from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,CreateView,FormView
from django.urls import reverse_lazy
from .forms import* 
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your views here.

# class MainHome(View):
#     def get(self,request,*args,**kwargs):
#         return render(request,"mainhome.html")

class MainHome(TemplateView):
    template_name="mainhome.html"
    
# class Registration(View):
#     def get(self,request,*args,**kwargs):
#         f=RegForm()
#         return render(request,"Registration.html",{'form':f})
#     def post(self,request,*args,**kwargs):
#         f=RegForm(data=request.POST)
#         if f.is_valid():
#             f.save()
#             messages.success(request,"SUCCESS")
#             return redirect("h")
#         else:
#             messages.error(request,"FAILED")
#             return render(request,"Registration.html",{'form':f})

class Registration(CreateView):
    form_class=RegForm
    template_name="Registration.html"
    model=User
    success_url=reverse_lazy("h")

class Login(FormView):
    template_name="login.html"
    form_class=LogForm
    # def get(self,request,*args,**kwargs):
    #     f=LogForm()
    #     return render(request,"login.html",{'form':f})
    def post(self,request,*args,**kwargs):
        form_data=LogForm(data=request.POST)
        if form_data.is_valid():
            us=form_data.cleaned_data.get("username")
            ps=form_data.cleaned_data.get("password")
            user=authenticate(request,username=us,password=ps)
            if user:
                login(request,user)
                messages.success(request,"LOGIN SUCCESSFUL")
                return redirect("uh")
            else:
                messages.error(request,"INCORRECT ENTRY!!")
                return redirect(request,"login.html",{"form":form_data})
        else:
            messages.error(request,"LOGIN FAILED!!")
            return render(request,"login.html",{"form":form_data})

class LogOut(View):
    def get(self,request):
        LogOut=(request)
        return render(request,"login.html")
    
class Reg(CreateView):
    form_class=RegForm
    template_name="Registration.html"
    model=User
    success_url=reverse_lazy("h")
    def form_valid(self, form):
        mail=form.cleaned_data.get("email")
        send_mail(
            "Around Me Registration",
            "Welcome to Around Me!!",
            "sachisouru@gmail.com",
            [mail]
        )
        messages.success(self.request,"Registration Successfull!!")
        self.objects=form.save()
        return super().form_valid(form)
        