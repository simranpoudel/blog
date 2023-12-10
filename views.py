from django.shortcuts import render ,redirect ,HttpResponse,get_object_or_404
from django.contrib.auth.models import User
from .models import Profile , Message ,Post ,Comment,Categorise
from django.contrib import messages
import random
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate , login, logout
from django.core.paginator import Paginator ,EmptyPage , PageNotAnInteger

code =0


def index(request):

    if request.user.is_authenticated:
        return redirect ('userhome')
    else:
        post = Post.objects.all().order_by('-date')
        post1 = []
        post1.extend(post[0:4])

        post2 = []
        post2.extend(post[4:8])
        post3 = []
        post3.extend(post[8:12])
        context = {
            'post1':post1,
            'post2':post2,
            'post3':post3
        }
        return render(request,'index.html',context)


def register(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        image1=request.FILES['image1']

        try:
            if User.objects.filter(username=username).first():
                messages.success(request,"User of this username is already exist ")
                return redirect('register')
            if User.objects.filter(email=email).first():
                messages.success(request," This email id is already is used ")
                return redirect('register')


            user_obj = User(first_name=firstname,last_name=lastname,username=username , email=email)
            user_obj.set_password(password)
            user_obj.save()
            global code
            code = random.randint(2000, 9000)
            profile_obj =Profile.objects.create(user=user_obj,code=code , profile_img=image1)
            profile_obj.save()
            # sendMail(email , code)
            return redirect('login')
        except Exception as e:
            messages.success(request, e)
            return redirect('register')




    return render(request,'register.html')

def login_attemp(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found plz create your account ')
            return redirect('login')
        else:
            profile_obj = Profile.objects.filter(user=user_obj).first()
            # if profile_obj.is_varified:
            user = authenticate(username=username,password=password)
            if user is None:
                messages.success(request, "Please enter correct password or username")
                return redirect('login')
            else:
                login(request, user)
                return redirect('userhome')


    return render(request,'login.html')


def verify(request):
    global code
    if request.method == "POST":
        code1=request.POST['code']


        # print("this is orginal code " + str(code))
        # print("this is optained code " + code1)

        if str(code) == code1:
            profile_obj =Profile.objects.filter(code=code).first()
            profile_obj.is_varified=True
            profile_obj.save()
            return redirect("login")
        else:
            messages.success(request, 'Please enter correct code')
            return redirect('mailsent')
    context={
        'code1':code
    }

    return render(request,'mailsent.html' , context )


def sendMail(email , code):
    subject ='Your account need to be varified'
    message = f'Hi !! Your configuration code is   '+  str(code)
    email_from = settings.EMAIL_HOST_USER
    recpient_list = [email]
    send_mail(subject,message,email_from,recpient_list)


def logout_attemp(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method=='POST':
        username= request.POST['name']
        email= request.POST['email']
        subject= request.POST['subject']
        msg= request.POST['message']
        try:
            mesg_obj = Message(username=username,email=email,subject=subject,mesg=msg)
            mesg_obj.save()
            messages.success(request, 'Your message is sent')
        except Exception as e :
            messages.success(request, e)
    return render(request, 'contact.html')

def dopost(request):
    caty = Categorise.objects.all()
    context = {
        'caty':caty
    }
    if request.method=="POST":
        title= request.POST['title']
        caty1= request.POST['caty']
        image= request.FILES['image']
        content= request.POST['content']
        user = request.user
        category = get_object_or_404(Categorise, name=caty1)
        post = Post.objects.create(title=title,caty=category,img =image,content = content , user=user)
        post.save()
        # messages.success(request,'Your Blog is successfully posted')
        return redirect('userhome')

    return render(request , 'dopost.html' , context)

def userhome(request):
    caty =Categorise.objects.all()
    post = Post.objects.all().order_by('-date')
    recentpost = []
    recentpost.extend(post[0:5])
    allpost = Paginator(post,2)
    page=request.GET.get("page")
    try:
        post=allpost.page(page)
    except PageNotAnInteger:
        post=allpost.page(1)
    except EmptyPage:
        post= allpost.page(allpost.num_pages)
    context = {
        'post':post,
        'caty':caty,
        'recentpost':recentpost,
     }
    return render(request, 'userhome.html',context)

def detailpage(request , id):
    post = Post.objects.filter(id =id).first()
    comment = Comment.objects.filter(post=post)
    context ={
        'post':post,
        'comment':comment
    }
    return render(request,'detailpage.html',context)

def comment(request):
    if request.method=="POST":
        comment =request.POST['comment']
        sno = request.POST['sno']
        post =Post.objects.get(id = sno)
        user = request.user
        comm = Comment.objects.create(comment=comment,user=user , post= post)
        comm.save()
        return redirect(f'/detailpage/{post.id}')

def myblog(request ,id):
    post1 = Post.objects.filter(user=id).order_by('-date')
    recentpost = []
    recentpost.extend(post1[0:8])
    allpost = Paginator(post1,2)
    page=request.GET.get("page")
    try:
        post=allpost.page(page)
    except PageNotAnInteger:
        post=allpost.page(1)
    except EmptyPage:
        post= allpost.page(allpost.num_pages)

    context = {
        'post':post,
        'recentpost':recentpost
    }
    return render(request, 'myblog.html',context)


def search(request):
    if request.method=="GET":
        key = request.GET['key']
        post = Post.objects.filter(Q(title__icontains=key) | Q(content__icontains=key))
        context={
                'post':post,
                'key':key
            }
        return render(request, 'search.html', context)


def category(request,id):
    caty =Categorise.objects.all()
    post1= Post.objects.filter(caty=id).order_by('-date')
    recentpost = []
    recentpost.extend(post1[0:5])
    allpost = Paginator(post1,2)
    page=request.GET.get("page")
    try:
        post=allpost.page(page)
    except PageNotAnInteger:
        post=allpost.page(1)
    except EmptyPage:
        post= allpost.page(allpost.num_pages)
    context = {
        'post':post,
        'caty':caty,
        'recentpost':recentpost
     }
    return render(request, 'category.html',context)

def deletepost(request,id):
    post = Post.objects.filter(id=id)
    post.delete()
    return redirect(f'/myblog/{post.user.id}')

def update(request, id ):
    caty = Categorise.objects.all()
    post = Post.objects.filter(id=id).first()
    if request.method=="POST":
        title= request.POST['title']
        caty1= request.POST['caty']
        content= request.POST['content']
        caty1= get_object_or_404(Categorise, name=caty1)
        post.title=title
        post.caty=caty1
        post.content=content
        post.save()
        # messages.success(request,'Your Blog is successfully updated')
        return redirect(f'/myblog/{post.user.id}')

    context ={
        'post':post,
        'caty':caty
    }
    return render(request, 'update.html', context)