from django.db.models import Count
from django.shortcuts import render
from .models import *
from django.shortcuts import render
from .forms import *  # 导入表单
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from .util import getcounts


# Create your views here.

def home(request):
    context = {
        'cats': Cat.objects.all()
    }
    return render(request, 'home.html', context)


def show_cat(request):
    c_id = request.GET.get('c_id')
    cat = Cat.objects.get(c_id=c_id)
    cat_r = CatRel.objects.filter(c_1=c_id)
    context = {
        'cat': cat,
        'cat_r': cat_r
    }
    return render(request, 'cat_profile.html', context)


def checkcat(request):
    checkcat_form = CheckcatForm()
    cats = Cat.objects.all()
    if not request.session.get('is_login', None):  # 不允许重复登录
        messages.warning(request, "请登录后打卡！")
        return render(request, 'home.html', locals())  # 自动跳转到首页

    if request.method == "POST":
        checkcat_form = CheckcatForm(request.POST)
        if checkcat_form.is_valid():  # 获取数据
            cat = checkcat_form.cleaned_data['cat']
            addr = checkcat_form.cleaned_data['addr']
            time = checkcat_form.cleaned_data['time']
            u_id = request.session['user_id']
            user = Userinfo.objects.get(u_id=u_id)

            new_checkcat = Checkcat.objects.create(c=cat, a=addr, k_time=time, u=user)
            new_checkcat.save()
            Cat.objects.filter(c_id=cat.c_id).update(a=addr, c_recent=time)
            message = "打卡成功！"

    return render(request, 'checkcat.html', locals())


def feed(request):
    feed_form = FeedForm()
    cats = Cat.objects.all()
    if not request.session.get('is_login', None):  # 不允许重复登录
        messages.warning(request, "请登录后投喂！")
        return render(request, 'home.html', locals())  # 自动跳转到首页

    if request.method == "POST":
        feed_form = FeedForm(request.POST)
        if feed_form.is_valid():  # 获取数据
            cat = feed_form.cleaned_data['cat']
            addr = feed_form.cleaned_data['addr']
            time = feed_form.cleaned_data['time']
            food = feed_form.cleaned_data['food']
            u_id = request.session['user_id']
            user = Userinfo.objects.get(u_id=u_id)

            new_feed = Feed.objects.create(f=food, c=cat, a=addr, t_time=time, u=user)
            new_feed.save()
            Cat.objects.filter(c_id=cat.c_id).update(a=addr, c_recent=time)
            message = "投喂成功！"

    return render(request, 'feed.html', locals())


def stat(request):
    c_stat = Checkcat.objects.values('c').annotate(counts=Count('c'))
    f_stat = Feed.objects.values('c').annotate(counts=Count('c'))
    catss = Cat.objects.all()
    cat_list = []
    for c in catss:
        time1 = getcounts(c_stat, c.c_id)
        time2 = getcounts(f_stat, c.c_id)
        ct = {
            'c_id': c.c_id,
            'c_name': c.c_name,
            'cc_time': time1,
            'f_time': time2,
            'time': time1 + time2,
        }
        cat_list.append(ct)
    return render(request, 'stat.html', locals())


def register(request):
    # 写注册方法
    register_form = RegisterForm()
    cats = Cat.objects.all()
    if request.session.get('is_login', None):  # 不允许重复登录
        return render(request, 'home.html', locals())  # 自动跳转到首页
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']

            if password1 != password2:  # 判断两次密码是否相同
                print("[DEBUG][POST][STATE]:两次输入的密码不同！")
                # message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_id_cus = Userinfo.objects.filter(u_name=username)
                # same_id_mng = StoreManager.objects.filter(manager_name=username)
                if same_id_cus:  # 用户名唯一
                    message = '用户名已经存在~请换一个'
                    return render(request, 'register.html', locals())
                # 当一切都OK的情况下，创建新用户
                else:
                    new_cus = Userinfo.objects.create(u_name=username,
                                                      u_password=password1)
                    new_cus.save()
                    # 自动跳转到登录页面
                    login_form = LoginForm()
                    messages.success(request, "注册成功！")
                    return render(request, 'login.html', locals())  # 自动跳转到登录页面
    else:
        return render(request, 'register.html', locals())
    return render(request, 'register.html', locals())


def login(request):
    login_form = LoginForm()
    cats = Cat.objects.all()
    if request.session.get('is_login', None):
        print("[DEBUG][POST][STATE]:已经登陆")
        return render(request, 'home.html', locals())

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # identy 表示
            print("[DEBUG][POST][LOGIN][username]:{}".format(username))
            print("[DEBUG][POST][LOGIN][password]:{}".format(password))
            try:
                print("[DEBUG][POST][STATE]:查询顾客用户数据库")
                user_cus = Userinfo.objects.get(u_name=username)
                if user_cus.u_password == password:
                    print("[DEBUG][POST][USERNAME]:{}".format(user_cus.u_name))
                    print("[DEBUG][POST][STATE]:登录成功")
                    messages.success(request, '{}登录成功！'.format(user_cus.u_name))
                    request.session['is_login'] = True
                    request.session['user_id'] = user_cus.u_id
                    request.session['user_name'] = user_cus.u_name
                    return render(request, 'home.html', locals())
                else:
                    print("[DEBUG][POST][STATE]:密码不正确")
                    message = "密码不正确"
            except:
                print("[DEBUG][POST][STATE]:用户不存在")
                message = "用户不存在"
    return render(request, 'login.html', locals())


def logout(request):
    # 写登出方法
    cats = Cat.objects.all()
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return render(request, 'home.html', locals())
    user_id = request.session['user_id']
    print("[DEBUG][REQUEST][退出]]")
    print("[DEBUG][REQUEST][USER_ID]:{}".format(user_id))
    try:
        user = Userinfo.objects.get(u_id=user_id)
        print("[DEBUG][REQUEST][退出]]：退出登录")
    except:
        print("[DEBUG][request][STATE]:退出错误，无法更新数据库中用户状态")

    request.session.flush()
    return render(request, 'home.html', locals())
