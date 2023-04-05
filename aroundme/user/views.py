from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,CreateView,UpdateView,FormView,DeleteView
from .forms import*
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Bio

# Create your views here.
# class UserHome(TemplateView):
#     # def get(self,request,*args,**kwargs):
#         # return render(request,"userhome.html")
#         template_name="userhome.html"
#         form_class=PostForm
#         model=Posts
        
class UserHome(CreateView):
    template_name="userhome.html"
    form_class=PostForm
    model=Posts
    success_url=reverse_lazy("uh")
    def form_valid(self,form):
        form.instance.user=self.request.user
        messages.success(self.request,"Post Uploaded")
        self.object=form.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["data"]=Posts.objects.all().order_by('-datetime')
        context["cform"]=CommentForm()
        context["comments"]=Comments.objects.all()
        return context
    
def addcomment(request,*args,**kwargs):
    if request.method=="POST":
        pid=kwargs.get("pid")
        post=Posts.objects.get(id=pid)
        user=request.user
        cmnt=request.POST.get("Comment")       
        Comments.objects.create(Comment=cmnt,user=user,post=post) 
        return redirect('uh')
    
def addlike(request,*args,**kwargs):
    pid=kwargs.get("pid")
    post=Posts.objects.get(id=pid)
    user=request.user
    post.likes.add(user)
    post.save()
    return redirect("uh")
    
class Profile(TemplateView):
    template_name="profile.html"
    
class BioView(CreateView):
    form_class=BioForm
    template_name="addbio.html"
    model=Bio
    success_url=reverse_lazy("pro")
    def form_valid(self, form):
        form.instance.user=self.request.user
        self.object=form.save()
        messages.success(self.request,"Bio Added...")
        return super().form_valid(form)


class EditBio(UpdateView):
    form_class=BioForm
    model=Bio
    template_name="editbio.html"
    success_url=reverse_lazy('pro')
    pk_url_kwarg="pk"
    
class EditPassword(FormView):
    template_name="changepassword.html"
    form_class=PChangeForm
    def post(self,request,*args,**kwargs):
        form_data=PChangeForm(data=request.POST)
        if form_data.is_valid():
            current=form_data.cleaned_data.get("c_password")
            new=form_data.cleaned_data.get("new_password")
            confirm=form_data.cleaned_data.get("conf_password")
            print(current)
            user=authenticate(request,username=request.user.username,password=current)
            if user:
                if new==confirm:
                    user.set_password(new)
                    user.save()
                    messages.success(request,"Password Changed")
                    logout(request)
                    return redirect("log")
                else:
                    messages.error(request,"Passwords Missmatches!!")
                    return redirect("editpass")
            else:
                messages.error(request,"Incorrect Password!!")
                return redirect("editpass")
        else:
            return render(request,"changepassword.html",{"form":form_data})
    
class MyPost(TemplateView):
    template_name="mypost.html"
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context["data"]=Posts.objects.all().order_by('-datetime')
        return context
    
class EditPost(UpdateView):
    form_class=PostForm
    model=Posts
    template_name="editpost.html"
    success_url=reverse_lazy('mypost')
    pk_url_kwarg="pk"
    
# class DeletePost(View):
#     def post(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         post=Posts.objects.get(id=id)
#         post.delete()
#         messages.success(request,"POST DELETED")
#         return redirect('mypost')

class DeletePost(DeleteView):
    model=Posts
    template_name="deletepost.html"
    success_url=reverse_lazy("mypost")
    
