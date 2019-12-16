from django.contrib import admin
from django.urls import path
from . import views
app_name = 'administer'
urlpatterns = [
    path('', views.register.as_view(),name='register'),
    path('redis/',views.test_redis,name="redis"),
    path('send_sms/',views.send_sms,name="send_sms"),
    path('check_sms/',views.check_sms,name="check_sms"),
    path('student_insex/',views.student_insex,name='student_insex'),
    path('teacher_login/',views.teacher_login,name='teacher_login'),
    path('student_list/',views.student_list.as_view(),name='student_list'),
    path('student_task/',views.student_task.as_view(),name='student_task'),
    path('publish/',views.publish.as_view(),name='publish'),
    path('viewjob/',views.viewjob,name="viewjob"),
    path('student_login/',views.student_login,name='student_login'),
    path('student_task_task/',views.student_task_task,name='student_task_task'),
    path('cancelled',views.cancelled,name='cancelled'),
    path('check/',views.check,name='check'),
    path('a_task/<pid>',views.a_task,name='a_task'),
]
