import json

from django.shortcuts import render
from .models import User,Task
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
# Create your views here.


@ensure_csrf_cookie
def ReactAppResponse(request, *args, **kwargs):
    return render(request, "./app.html")


def serialize_task(task):
    return {
        "id": task.id,
        "title": task.Title,
        "description": task.Description,
        "completed": task.completed,
        "priority": getattr(task, "priority", "Medium") or "Medium",
        "due_date": getattr(task, "due_date", "") or "",
        "user_id": task.user_id,
    }


def json_body(request):
    if not request.body:
        return {}
    return json.loads(request.body.decode("utf-8"))


def user_payload(user):
    tasks = Task.objects.filter(user_id=user.id).order_by("id")
    return {
        "user": {"id": user.id, "username": user.Username},
        "tasks": [serialize_task(task) for task in tasks],
        "count": tasks.filter(completed=False).count(),
    }
def IndexPageResponse(request):
    return ReactAppResponse(request)


def RegisterPageResponse(request):
    return ReactAppResponse(request)


def InsertUserDetails(request):
    username = request.POST['username']
    password = request.POST['password']
    confirm = request.POST['confirm']

    if password != confirm:
        return render(request, "./register.html",
                      context={'error': 'Passwords do not match'})

    if User.objects.filter(Username=username).exists():
        return render(request, "./register.html",
                      context={'error1': 'Try a different username'})

    obj = User()
    obj.Username = username
    obj.Password = password
    obj.save()

    return render(request, "./index.html")


def dashboard(request,id):
    return ReactAppResponse(request)


def dashboardPageResponse(request):
    username = request.POST['username']
    password = request.POST['password']

    try:
        obj=User.objects.get(Username=username)

        if obj.Password == password:
            tasks = Task.objects.filter(user_id=obj.id)
            count = Task.objects.filter(user_id=obj.id, completed=False).count()

            return render(request,"./dashboard.html",{'id': obj,'task': tasks,'count': count})
        else:
            return render(request, "./index.html", {'error1': 'Invalid password'})

    except User.DoesNotExist:
        return render(request, "./index.html", {'error': 'Invalid username'})
            

    
def taskPageResponse(request,id):
    return ReactAppResponse(request)


    
def insertTaskPageResponse(request,id):
    completed=None
    title=request.POST['title']
    desc=request.POST['desc']
    obj=Task()
    if title=='':
         obj.Title="untitled"
    else:
        obj.Title=title
    obj.Description=desc
    obj.user_id=id
    obj.save()
    task=Task.objects.filter(user_id=id)
    user=User.objects.get(id=id)
    count = Task.objects.filter(user_id=user.id, completed=False).count()
    return render(request,"./dashboard.html",context={'task':task,'id':user,'count':count})


def updatepageresponse(request,id):
    return ReactAppResponse(request)


def updateTaskResponse(request,task_id):
    task=Task.objects.get(id=task_id)
    task.Title= request.POST['title']
    task.Description=request.POST['desc']
    task.completed = "completed" in request.POST
    task.save()
    task1=Task.objects.filter(user_id=task.user_id)
    user=User.objects.get(id=task.user_id)
    count = Task.objects.filter(user_id=user.id, completed=False).count()
    return render(request,"./dashboard.html",context={'task':task1,'id':user,'count':count})

def deleteTaskPageResponse(request,id):
    return ReactAppResponse(request)

def delTaskRespaonse(request,id):
    task=Task.objects.get(id=id)
    tasks=Task.objects.filter(user_id=task.user_id)
    task.delete()
    tasks=Task.objects.filter(user_id=task.user_id)
    user=User.objects.get(id=task.user_id)
    count = Task.objects.filter(user_id=user.id, completed=False).count()
    return render(request,"./dashboard.html",context={'task':tasks,'id':user,'count':count})
    


















    

def delte_all_task(request):
    obj=Task.objects.all()
    obj.delete()
    return HttpResponse("all the record deleted")


@require_http_methods(["POST"])
@csrf_exempt
def api_register(request):
    data = json_body(request)
    username = data.get("username", "").strip()
    password = data.get("password", "")
    confirm = data.get("confirm", "")

    if not username or not password or not confirm:
        return JsonResponse({"error": "Please fill all fields"}, status=400)

    if password != confirm:
        return JsonResponse({"error": "Passwords do not match"}, status=400)

    if User.objects.filter(Username=username).exists():
        return JsonResponse({"error": "Try a different username"}, status=400)

    user = User.objects.create(Username=username, Password=password)
    return JsonResponse(user_payload(user), status=201)


@require_http_methods(["POST"])
@csrf_exempt
def api_login(request):
    data = json_body(request)
    username = data.get("username", "").strip()
    password = data.get("password", "")

    try:
        user = User.objects.get(Username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid username"}, status=400)

    if user.Password != password:
        return JsonResponse({"error": "Invalid password"}, status=400)

    return JsonResponse(user_payload(user))


@require_http_methods(["GET"])
def api_user_tasks(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse(user_payload(user))


@require_http_methods(["GET"])
def api_task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    return JsonResponse({"task": serialize_task(task)})


@require_http_methods(["POST"])
@csrf_exempt
def api_create_task(request, user_id):
    data = json_body(request)
    title = data.get("title", "").strip() or "untitled"
    description = data.get("description", "")
    completed = bool(data.get("completed", False))
    priority = data.get("priority", "Medium")
    if priority not in ["High", "Medium", "Low"]:
        priority = "Medium"
    due_date = str(data.get("due_date", "") or "")[:20]

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    Task.objects.create(
        Title=title[:20],
        Description=description,
        completed=completed,
        priority=priority,
        due_date=due_date,
        user_id=user.id,
    )
    return JsonResponse(user_payload(user), status=201)


@require_http_methods(["POST"])
@csrf_exempt
def api_update_task(request, task_id):
    data = json_body(request)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    task.Title = (data.get("title", "").strip() or "untitled")[:20]
    task.Description = data.get("description", "")
    task.completed = bool(data.get("completed", False))
    priority = data.get("priority", task.priority or "Medium")
    if priority in ["High", "Medium", "Low"]:
        task.priority = priority
    task.due_date = str(data.get("due_date", task.due_date or "") or "")[:20]
    task.save()

    user = User.objects.get(id=task.user_id)
    return JsonResponse(user_payload(user))


@require_http_methods(["POST"])
@csrf_exempt
def api_toggle_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    task.completed = not task.completed
    task.save()

    user = User.objects.get(id=task.user_id)
    return JsonResponse(user_payload(user))


@require_http_methods(["POST"])
@csrf_exempt
def api_delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    user = User.objects.get(id=task.user_id)
    task.delete()
    return JsonResponse(user_payload(user))
