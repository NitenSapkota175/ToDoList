from django.urls import path
from . views import TaskDelete, TaskList,TaskDetail,TaskCreate,TaskUpdate,CustomLoginView,RegisterPage
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page ='login'),name='logout'), #it just need get request and where you want to send the user to the login page by specifing the next_page value  and set the usrl to the logout page 
    path('register/',RegisterPage.as_view(),name='register'),

    path('',TaskList.as_view(),name = 'tasks'), #our url resolver can't use a class inside of it so what we need to is use a method  that this view  has right here and we want to trigger  the as_view() method and that is going to trigger function inside of that view depending on the method type as post or get request 
    path('task/<int:pk>',TaskDetail.as_view(),name = 'task'),#in this case view by default looks for primary key so Pk value in this we set that as a integer 
    path('create-task',TaskCreate.as_view(),name = 'task-create'),
    path('update-task/<int:pk>',TaskUpdate.as_view(),name = 'task-update'),
    path('update-delete/<int:pk>',TaskDelete.as_view(),name = 'task-delete'),
]