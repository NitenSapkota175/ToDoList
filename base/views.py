from asyncio import Task
from pickle import NONE
from re import template
from attr import fields
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView 
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin #this mixin is used to restric the user to go into certain pages 
from django.contrib.auth.forms import UserCreationForm #this is built in form we dont builtin classview in django so we will use this 
from django.contrib.auth import login
from matplotlib.pyplot import title 
from . models import Task
# Create your views here.

# Create your views here.
'''
what are class based views ?
 
 In short django class based views are simply djago views written as python classes 
 At the end of all views are functions but htis encapsulated inside of class and we are utlies a
 things like inheritence we are able to multiple inheritence we are also write more reuseable code 

 read the artical go to the video you have watched and are links in the description 

 The view we are going to use is a ListView this is the view built in with django and this view is 
 incharge of returning back a query set and a template   


 DetailView takes in the id from the url parameter or slug field  when e trigger the views that inherit 
 from it already knows how get a product deatils and how to render a template san how to pull of the
 information 


 CreateView actually uses model forms it already has the model form built in to it in this case we 
 can use our own 

 UpdateView is similar to the create views


 DeleteView  after deleting anything its redirect the user to after deleting it ,it task a get request 
 render a templates like confirmation 

 this are the most comman vies along with authrntication views   

 This are created to make easier the basic functionality for us 

  To undersatnd how class based view work we wann understand how they are constursted so calssed based 
  views are collections of mixin and other views so there lot of inheriting going on and a combine set
  of mixin and view create every single view to giv it functionality 

  mixin is class that is design to provid  certain level of functionality and is supossed to one thing
  if we see that we do over and over again we can create a speicfic mixin and use that into a class 
  that we give us specific action that we can performe it just extends our classes 

  we can over ride all of deault settings in built views 
 
      Related Article: https://www.dennisivy.com/post/django...
'''

class CustomLoginView(LoginView):
   template_name = 'base/login.html'
   #by default it provides the login form
   fields = '__all__'
   #if the user is authenticated it doesn't allow the user here so this just another attribute to this view
    
   redirect_authenticated_user = True  # by default it is false 

   #i wanna override the success url 
   def get_success_url(self):
      return reverse_lazy('tasks')

   # here we created a customview for login but we can directly use that in url we will do that with logout view
class RegisterPage(FormView):
   template_name = 'base/register.html'
   form_class = UserCreationForm
   redirect_authenticated_user = True 
   success_url = reverse_lazy('tasks')

   #now i want to redirect the user once they have rigeester
   def form_valid(self,form):
      user = form.save()
      if user is not None:
         login(self.request,user)
      return super(RegisterPage,self).form_valid(form)

   def get(self,*args,**kwargs):
      if self.request.user.is_authenticated:
         return redirect('tasks')
      return super(RegisterPage,self).get(*args,**kwargs)
         

#now if you try to access tasklist without login then it say pagenot found but what we want to do is if the user try access without login we want to redirect the user to the login page so to that we have go to the settings.py file and and do this LOGIN_URL = 'login' 
class TaskList(LoginRequiredMixin,ListView): #we have to add that before the view 
   model = Task  # we haven't define the template yet and if we run a server by default it looks for bas/task_list.html (perfix of model name task or whatever you rmodel name is ) that we haven't define yet 
   #how does the django passed in the query set ? by default django calls that query set object list(look at the article above ) by default django gonna look for objects _list and i wanna customise this name too  
   context_object_name = 'tasks'

   def get_context_data(self, **kwargs): # we are overiding this function the super is just the another function of this method  ,The default implementation adds the object being displayed to the template, but you can override it to send more
       #Call the base implementation first to get a context
       context =  super().get_context_data(**kwargs)
       
       #The super() function is used to give access to methods and properties of a parent or sibling class.

       #The super() function returns an object that represents the parent class.

        # Add in a QuerySet of spefic user
       context['tasks'] = context['tasks'].filter(user=self.request.user)
       context['count'] = context['tasks'].filter(complete = False).count() #the reason we are doign is we want to the count of incomplete items here ,the reason we dont have to send in the use here is now because we are filtering the above set of data down here we are filtering filtered queryset 
       
       search_input = self.request.GET.get("search-area") or ''
       if search_input :
          context['tasks'] = context['tasks'].filter(title__startswith=search_input)
       context['search_input'] = search_input
       return context
       
       return context 

#DeatilView is simple a view that returns back information about a simple item so when we click on task we wann get more information about this item so lets say we go to url task/id we want o pull information about that task 
class TaskDetail(LoginRequiredMixin,DetailView):
   model = Task
   #so now this voew looks for a template the prefix of the model name task_deatil.html 
   # for a query set task_list it looks for oject_lsit in this by default is looks for object we can customise it 
   context_object_name = 'task'
   template_name = 'base/task.html' #we change the default task name from task_detail.html to task.html  

 

class TaskCreate(LoginRequiredMixin,CreateView):
   model = Task #by default createview uses model form and by default it look for a name task_form.html ,we just to speify the feilds we want to use 
   fields = ['title','description','complete']
   #i also want to make user whenever the user submit the form ,we can redirect the user to different page we also need to add that to the create view 
   #and i want create a import here this is gonna be import calledreverse_lazy which just redirect the user to our certian page or application 
   #django already create a form by default the form name is form and it passes that form o template by default
   
   #if the user created a task we need to set that user automatically to the task he or she have created so do that we need to override the method form_valid
   def form_valid(self,form): #this method is going get triggered by post request by default
    form.instance.user =  self.request.user
    return super(TaskCreate,self).form_valid(form) 
   
   success_url = reverse_lazy('tasks')

#UpdateView  is is supossed to take in an item it is supossed  to prefill a form and once we submit it just like the create view creates an items updateview supossed to midfy the data 
class TaskUpdate(LoginRequiredMixin,UpdateView):
   model = Task
   fields = ['title','description','complete']
   success_url = reverse_lazy('tasks')

  

#DeleteView is like a confimation page it does two things  it renders out  a page that says are you yu want to delte this item? and when we send a post request it going to delete that item 
class TaskDelete(LoginRequiredMixin,DeleteView):
   model = Task
   context_object_name = 'task'
   #by default it looks for tempalte of prefix name of model name and suffix of confirm_delete (task_confirm_delete.html)
   
   success_url = reverse_lazy('tasks')

