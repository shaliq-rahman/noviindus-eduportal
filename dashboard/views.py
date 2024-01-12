from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Course
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import *
from django.shortcuts import get_object_or_404
from django.db import transaction
from .helper import is_ajax
from django.contrib.auth.models import User
from django.contrib import messages



# Create your views here.
def index(request):
    return render(request, 'index.html')


def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'dashboard/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


class Dashboard(LoginRequiredMixin,View):
    template_name = "dashboard/index.html"
    def get(self, request, *args, **kwargs):
        datas = {}
        return render(request, self.template_name, datas)
    

class ProfileView(LoginRequiredMixin,View):
    template_name = "dashboard/profile/index.html"
    def get(self, request, *args, **kwargs):
        datas = {}
        datas['user_id']= request.user.id
        return render(request, self.template_name, datas)
    
    def post(self, request, *args, **kwargs):
        userid = request.POST.get('user_id')
        current_passowrd =  request.POST.get('current_passowrd')
        pwd = request.POST.get('new_password')
        cpwd = request.POST.get('confirm_password')

        try:
            user = User.objects.get(pk=userid)
        except User.DoesNotExist:
            user = None
        if pwd == cpwd:
        
            if user:
                user.set_password(pwd)
                user.save()
                messages.success(request, 'password change success')
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Please Try again')
                return render(request, 'dashboard/profile/index.html')

        else:
            messages.error(request, "password doesnot match")
            return render(request, 'dashboard/profile/index.html')

    

class ShortTermCourses(LoginRequiredMixin, View):
    template_name = "dashboard/courses/index.html"
    
    def get(self, request, *args, **kwargs):
        filter_conditions = {}
        
        if is_ajax(request=request):
            query = request.GET.get('query', None)
            filter_conditions['title__icontains'] = query
            
        courses = Course.objects.filter(**filter_conditions)
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            page = 1

        paginator = Paginator(courses, 2)

        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)  
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)
            
        if is_ajax(request=request):
            context = {}
            context['courses']= courses
            response = {"status": True,
                        "pagination": render_to_string("dashboard/courses/courses_pagination.html", context=context, request=request),
                        "template": render_to_string("dashboard/courses/courses_list.html", context, request=request),}
            return JsonResponse(response)
            
        datas = {'courses':courses, 'current_page': page}
        return render(request, self.template_name, datas)
    

class CourseCreate(LoginRequiredMixin, View):
    template_name = "dashboard/courses/course_form.html"

    def get(self, request, *args, **kwargs):
        data = {}
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        response = {}
       
        try:
            with transaction.atomic():
                create_conditions, data = {}, {}
                title = request.POST.get('title', None)
                subtitle = request.POST.get('subtitle', None)
                description = request.POST.get('description', None)
                amount = request.POST.get('amount', None)
                status = request.POST.get('status', None)
                course_image = request.FILES.get('course_image', None)
                
                # CHECK THE DATA EXISTS
                if Course.objects.filter(title=title).exists():
                    data['status'] = False
                    data['message'] = 'Data already exists'
                else:
                    if title:
                        create_conditions['title']= title
                    if subtitle:
                        create_conditions['subtitle']= subtitle
                    if description:
                        create_conditions['description']= description
                    if amount:
                        create_conditions['amount']= amount
                    if status:
                        create_conditions['is_active']= True
                    if course_image:
                        create_conditions['image']= course_image
                    Course.objects.create(**create_conditions)
                    data['status'] = True
                    data['message'] = 'course created successfully'
                    data['redirect_url'] = '/courses/'
        except Exception as error:
            response["status"] = False
            response["message"] = "Something went wrong"
       
        return JsonResponse(data)
    
    

class CourseEdit(LoginRequiredMixin, View):
    template_name = "dashboard/courses/course_form.html"

    def get(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, id=course_id)
        context = {'course': course, 'id':course_id}
        return render(request, self.template_name, context)

    def post(self, request, course_id, *args, **kwargs):
        response = {}
        try:
            with transaction.atomic():
                update_conditions, data = {}, {}
                
                # Retrieve data from the POST request
                title = request.POST.get('title', None)
                subtitle = request.POST.get('subtitle', None)
                description = request.POST.get('description', None)
                amount = request.POST.get('amount', None)
                status = request.POST.get('status', None)
                course_image = request.FILES.get('course_image', None)
                
                # CHECK THE DATA EXISTS
                if Course.objects.exclude(id=course_id).filter(title=title).exists():
                    data['status'] = False
                    data['message'] = 'Data already exists'
                else:
                    if title:
                        update_conditions['title'] = title
                    if subtitle:
                        update_conditions['subtitle'] = subtitle
                    if description:
                        update_conditions['description'] = description
                    if amount:
                        update_conditions['amount'] = amount
                    if status:
                        update_conditions['is_active'] = True
                    if course_image:
                        update_conditions['image'] = course_image
                    
                    # Update the existing course instance
                    Course.objects.filter(id=course_id).update(**update_conditions)
                    print('pppojoj')
                    
                    data['status'] = True
                    data['message'] = 'Course updated successfully'
                    data['redirect_url'] = '/courses/'
        except Exception as error:
            response["status"] = False
            response["message"] = "Something went"
        return JsonResponse(data)
    
    
    
class CourseDelete(LoginRequiredMixin, View):
    template_name = "dashboard/courses/course_form.html"

    def get(self, request, course_id, *args, **kwargs):
        response = {}
        try:
            with transaction.atomic():
                course = get_object_or_404(Course, id=course_id)
                course.delete()
                return HttpResponseRedirect('/courses/')
        except Exception as error:
            response["status"] = False
            response["message"] = f"Error: {error}"

        return JsonResponse(response)
