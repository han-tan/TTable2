from django.shortcuts import render,redirect
from django.http import request
from django.http.response import HttpResponse
# 导入缓存对象
from django.core.cache import cache
from utils import aliyunsms, restful
from .models import *
from django.views import View
from django.core.paginator import Paginator
import json
# 首页显示验证码

from captcha.helpers import captcha_image_url

def check(request):
    # print('验证用户名是否存在')
    uname = request.GET['uname']
    print('用户名:',uname)
    #链接数据库
    if Student.objects.filter(name=uname):
        print('已占用')
        return  HttpResponse(json.dumps({'result':'false'}))
    else:
            # 向前台返回的是json结果
        return  HttpResponse(json.dumps({'result':'true'}))

class register(View):
    def get(self,request):
        # 跳转页面时,初始化图文验证码表单项,传递到index页面
        return render(request, 'register.html', locals())
    def post(self,request):
        username = request.POST.get('user_name')
        password = request.POST.get('user_password')
        # print(username, password)
        phone = request.POST.get('phone')
        Student.objects.create(name=username,password=password,phone=phone)
        return redirect('administer:student_login')

# 个人信息
# def Personal(request):
#     id = request.POST.get('id')
#     personal = Task.objects.get(student_id=id)


def teacher_login(request):
    if request.method =="POST":
        username = request.POST.get('username')
        passed = request.POST.get('pwd')
        print(username,passed)
        # print(Teacher.objects.name)
        try:
            user = Teacher.objects.get(name=username)
        except:
            return render(request,'teacher_login.html',{'error':'用户名错误'})
        if user.password==passed:
            return render(request,'index.html',{"user":username})
        return render(request,'teacher_login.html',{"error":'密码错误'})
    else:
        return render(request,'teacher_login.html')

class student_list(View):
    def get(self,request):
        data = Student.objects.all()
        return render(request,'Student_list.html',{'data':data})
class student_task(View):
    def get(self,request):
        return render(request,'Student_task.html')

class publish(View):
    def get(self,request):
        return render(request,'publish.html')
    def post(self,request):
        task_name = request.POST.get('task_name')
        gcontent = request.POST.get('gcontent')
        print(task_name,gcontent)
        Task.objects.create(task_name=task_name,task_description=gcontent)
        print('cc')
        return redirect('administer:student_task')

def viewjob(request):
    list = Task.objects.all()
    return render(request,'viewjob.html',{'data':list})


def student_login(request):
    if request.method =="POST":
        username = request.POST.get('username')
        passed = request.POST.get('pwd')
        print(username,passed)
        print(Teacher.objects.name)
        try:
            user = Student.objects.get(name=username)
        except:
            return render(request,'student_login.html',{'error':'用户名错误'})
        if user.password==passed:
            return render(request,'student_information.html',{"user":username})
        return render(request,'student_login.html',{"error":'密码错误'})
    else:
        return render(request,'student_login.html')


def student_task_task(request):
    list = Task.objects.all()
    return render(request,'student_task_task.html',{'data':list})

def cancelled(request):
    return redirect('administer:register')

# 测试Redis存储
def test_redis(request):
    # 使用缓存对象,操作Redis
    cache.set('name', 'tom', 60)  # 存
    print(cache.has_key('name'))  # 判断
    print(cache.get('name'))  # 获取

    return HttpResponse("测试Redis")


# 发送短信
def send_sms(request):
    # 接口地址:/duanxin/send_sms/?phone=xxxx
    # 1 获取手机
    phone = request.GET.get('phone')
    print('手机:' + phone)
    # 2 生成6位随机码
    code = aliyunsms.get_code(6, False)
    # 3 缓存到redis
    cache.set(phone, code, 30 * 60)  # 60s有效
    print('是否写入redis成功:', cache.has_key(phone))
    print('打印code:', cache.get(phone))
    # 4 发短信
    result = aliyunsms.send_sms(phone, code)
    return HttpResponse(result)


# 短信验证
def check_sms(request):
    # /duanxin/check_sms/?phone=xxx&code=xx
    # 1 后去电话和code
    phone = request.GET.get('phone')
    code = request.GET.get('code')
    # 2 获取Resis中code
    cache_code = cache.get(phone)
    # 3 判断
    if code == cache_code:
        return restful.page_error("OK", data=None)
    else:
        return restful.page_error("False", data=None)

def student_insex(request):
    return render(request,'student_information.html')


def bad_request(request):
    return render(request, 'page_400.html')


def permission_denied(request):
    return render(request, 'page_403.html')


def page_not_found(request):
    return render(request, 'page_404.html')


def server_error(request):
    return render(request, 'page_500.html')



def a_task(request,pid):
    print(pid)
    stu_task = StudentTask.objects.get(studennt_id=pid)

    stu_task2_id= stu_task.task_id
    task = Task.objects.get(id=stu_task2_id)
    stu_name = task.task_name
    print(stu_name)
    stu_whether_complete = stu_task.whether_complete
    if stu_whether_complete=='否':
        complete = 50
    else:
        complete = 100
    return render(request,'a_task.html',{"stu_task":stu_name,"stu_name":stu_whether_complete,'complete':complete})

