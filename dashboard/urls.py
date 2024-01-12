from django.urls import path
from .views import *
app_name='dashboard'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='user_login'),
    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('courses/', ShortTermCourses.as_view(), name='short_term_courses'),
    path('courses/add/', CourseCreate.as_view(), name='course_create'),
    path('courses/<str:course_id>/edit/', CourseEdit.as_view(), name='course_edit'),
    path('courses/<str:course_id>/delete/', CourseDelete.as_view(), name='course_delete'),
    
]