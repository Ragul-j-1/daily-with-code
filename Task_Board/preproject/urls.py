"""
URL configuration for preproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rag1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/register", views.api_register),
    path("api/login", views.api_login),
    path("api/users/<int:user_id>/tasks", views.api_user_tasks),
    path("api/tasks/<int:task_id>", views.api_task_detail),
    path("api/tasks/<int:user_id>/create", views.api_create_task),
    path("api/tasks/<int:task_id>/update", views.api_update_task),
    path("api/tasks/<int:task_id>/toggle", views.api_toggle_task),
    path("api/tasks/<int:task_id>/delete", views.api_delete_task),
    path("",views.IndexPageResponse),
    path("login",views.IndexPageResponse),
    path("dash-<int:id>",views.dashboard,name="dasboard"),
    path("register",views.RegisterPageResponse),
    path("insuser",views.InsertUserDetails),
    path("dashboard",views.dashboardPageResponse),
    path("createtask-<int:id>",views.taskPageResponse),
    path("insert-<int:id>",views.insertTaskPageResponse,),
    path("update-<int:id>",views.updatepageresponse),
    path("updated-<int:task_id>",views.updateTaskResponse),
    path("delpage-<int:id>",views.deleteTaskPageResponse),
    path("deltask-<int:id>",views.delTaskRespaonse),
    #path("deltask",views.delte_all_task)

]
