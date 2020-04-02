#from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from sistema.serializers import *
from rest_framework import generics, permissions
from rest_framework import viewsets
#from rest_auth.registration.views import RegisterView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic.detail import DetailView
from .forms import SignInForm
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def create(self, request, *args, **kwargs):
        super(PostViewSet, self).create(request, *args, **kwargs)
        # here may be placed additional operations for
        # extracting id of the object and using reverse()
        return HttpResponseRedirect(redirect_to='/api/newpost/')

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    #def create(self, request, *args, **kwargs):
        #response=super(ImageViewSet, self).create(request, *args, **kwargs)
        #return HttpResponseRedirect(redirect_to='/api/rest/posts/'+str(response.post.id)+'/addimages/')

# desplegar una imagen en el archivo imagen.html
def image(request,pk):
    form = ContactForm()
    formr = ResponseForm()
    formar = CommentRepliesForm()
    template = get_template('image.html')
    username = request.user.username
    if not username:
        username = None
    comr=list()
    isBreak= True
    try:
        post = Post.objects.get(pk=pk)
        try:
            comment = Comment.objects.filter(post=post)
        except Comment.DoesNotExist:
            comment = 0
        try:
            img = Image.objects.filter(post=post)
        except Image.DoesNotExist:
            img = 0
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    if comment != 0:
        replies =Response.objects.all()
        #for reply in replies:
            #comr.append(reply.comment)
        if replies.count==0:
            replies = 0
    if request.method=='GET':
        html = template.render({'img': img, 'post': post, 'comment':comment, 'form':form, 'formr':formr,
                        'comr':comr,'replies':replies,'formar':formar,'username':username }, request)
        return HttpResponse(html)

    elif request.method == 'POST':
        if request.POST['flag']=="responder":
            if request.user.is_staff and request.user.is_superuser:
                try:
                    com = Comment.objects.get(pk=request.POST['primarkey'])
                except Comment.DoesNotExist:
                    com = 0
                formr = ResponseForm(data=request.POST)
                formr.fields['respuesta'].error_messages = {'required': 'Este campo es requerido'}
                if formr.is_valid():
                    usr = request.user.username
                    if (not request.user.username):
                        usr = "Anónimo"
                    Response.objects.create(repliedBy=usr, text=request.POST['respuesta'], comment=com)
                return HttpResponseRedirect("/api/rest/posts/" + str(post.id) + "/image/")
            else:
                return HttpResponse('Forbidden access', status=403)
        elif  request.POST['flag']=="comentar":
            form = ContactForm(data=request.POST)
            form.fields['mensaje'].error_messages = {'required': 'Este campo es requerido'}
            if form.is_valid():
                usr = request.user.username
                if (not request.user.username):
                    usr = "Anónimo"
                Comment.objects.create(createdBy=usr, text=request.POST['mensaje'], post=post)
            return HttpResponseRedirect("/api/rest/posts/" + str(post.id) + "/image/")
@login_required
def addimages(request,pk):
    if request.user.is_superuser and request.user.is_staff:
        formi = ImageForm()
        formar = CommentRepliesForm()
        formr = ResponseForm()
        template = get_template('addimages.html')
        username = request.user.username
        if not username:
            username = None
        try:
            post = Post.objects.get(pk=pk)
            try:
                comment = Comment.objects.filter(post=post)
            except Comment.DoesNotExist:
                comment = 0
            try:
                img = Image.objects.filter(post=post)
            except Image.DoesNotExist:
                img = 0
        except Post.DoesNotExist:
            return HttpResponse(status=404)
        responses=Response.objects.all()
        if responses.count()==0:
            responses=0
        if request.method == 'GET':
            html = template.render({'img': img, 'post': post,'formar':formar,
            'formr':formr,'responses':responses,'comment':comment,'formi': formi, 'username': username}, request)
            return HttpResponse(html)
        elif request.method == 'POST':
            if request.POST['flag']=="add":
                imagePath = request.FILES['imagePath']
                posturl = "/api/rest/posts/" + str(request.POST['postid']) + "/"
                data = {'imagePath': imagePath, 'post': posturl}
                serializer = ImageSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
                    return HttpResponse('Bad Request', status=400)
                return HttpResponseRedirect("/api/rest/posts/" + str(post.id) + "/addimages/")
            elif request.POST['flag']=="delete":
                Comment.objects.filter(pk=request.POST['commentid']).delete()
                return HttpResponseRedirect("/api/rest/posts/" + str(post.id) + "/addimages/")
            elif request.POST['flag']=="deleteresponse":
                Response.objects.filter(pk=request.POST['primarkey']).delete()
                return HttpResponseRedirect("/api/rest/posts/" + str(post.id) + "/addimages/")
    else:
        return HttpResponse('Forbidden access', status=403)
def home(request):
    template = get_template('home.html')
    img=Image.objects.all()[0:8]
    username = request.user.username
    if not username:
        username = None
    if request.method=='GET':
        html = template.render({'img': img, 'username':username}, request)
        return HttpResponse(html)
def about(request):
    template = get_template('about.html')
    img=Image.objects.all()[0:8]
    username = request.user.username
    if not username:
        username = None
    if request.method=='GET':
        html = template.render({'img': img, 'username':username}, request)
        return HttpResponse(html)
#create a new post and retrieve all posts
@login_required
def post(request):
    if request.user.is_superuser and request.user.is_staff:
        formp = PostForm()
        allposts = Post.objects.all()
        username = request.user.username
        if not username:
            username = None
        template = get_template('createpost.html')
        if request.method == 'GET':
            html = template.render({'formp': formp, 'allposts': allposts, 'username': username}, request)
            return HttpResponse(html)
    else:
        return HttpResponse('Forbidden access', status=403)
@login_required
def singleservice(request,pk):
    if request.user.is_superuser and request.user.is_staff:
        forms = ServiceForm()
        formd = DeleteService()
        users = get_user_model().objects.filter(is_superuser=False, is_staff=False)
        username = request.user.username
        service=Service.objects.get(pk=pk)
        if not username:
            username = None
        template = get_template('servicedata.html')
        if request.method == 'GET':
            html = template.render({'formd':formd,'forms': forms, 'users': users, 'username': username,'service':service}, request)
            return HttpResponse(html)
        elif request.method == 'POST':
            if request.POST['delete']=="update":
                usr=get_user_model().objects.get(pk=request.POST['userid'])
                try:
                     service.name = request.POST['name']
                     service.cost = request.POST['cost']
                     service.description = request.POST['description']
                     service.percentage = request.POST['percentage']
                     service.user =usr
                     service.save()
                except Service.DoesNotExist:
                     pass
                return HttpResponseRedirect(redirect_to='/api/rest/services/' + str(pk) + '/data/')
            elif request.POST['delete']=="delete":
                Service.objects.filter(pk=pk).delete()
                return HttpResponseRedirect(redirect_to='/api/rest/services/'+str(service.user.id)+'/addservices/')

    else:
        return HttpResponse('Forbidden access', status=403)

@login_required
def singlepayment(request,pk):
    if request.user.is_superuser and request.user.is_staff:
        forms = ServiceForm()
        formd = DeleteService()
        services = Service.objects.all()
        username = request.user.username
        payment=Payment.objects.get(pk=pk)
        if not username:
            username = None
        template = get_template('paymentdata.html')
        if request.method == 'GET':
            html = template.render({'formd':formd,'forms': forms, 'services': services, 'username': username,'payment':payment}, request)
            return HttpResponse(html)
        elif request.method == 'POST':
            if request.POST['delete']=="update":
                service=Service.objects.get(pk=request.POST['serviceid'])
                try:
                     payment.date = request.POST['date']
                     payment.amountPaid = request.POST['amountPaid']
                     payment.total = service.cost
                     payment.service =service
                     payment.save()
                     pays = Payment.objects.filter(service=service)
                     totalp = 0
                     for pay in pays:
                         totalp = totalp + pay.amountPaid
                     totalRemaining = service.cost - totalp
                     payment.totalRemaining = totalRemaining
                     payment.save()
                except Payment.DoesNotExist:
                     pass
                return HttpResponseRedirect(redirect_to='/api/rest/payments/' + str(pk) + '/data/')
            elif request.POST['delete']=="delete":
                Payment.objects.filter(pk=pk).delete()
                return HttpResponseRedirect(redirect_to='/api/rest/payments/'+str(payment.service.id)+'/addpayments/')

    else:
        return HttpResponse('Forbidden access', status=403)
@login_required
def payments(request,pk):
    if request.user.is_superuser and request.user.is_staff:
        formp = PaymentForm()
        ser = Service.objects.get(pk=pk)
        payments=Payment.objects.filter(service=ser)
        u=ser.user
        username = request.user.username
        if not username:
            username = None
        if not payments:
            payments = None
        template = get_template('createpayment.html')
        if request.method == 'GET':
            html = template.render({'ser':ser,'u':u,'formp': formp, 'payments':payments,'username': username}, request)
            return HttpResponse(html)
        elif request.method == 'POST':
            total=ser.cost
            allpaysservice=Payment.objects.filter(service=ser)
            totalpayed=0
            amountPaid=request.POST['amountPaid']
            for pay in allpaysservice:
                totalpayed = totalpayed + int(pay.amountPaid)
            totalpayed = totalpayed + int(amountPaid)
            totalRemaining=total-totalpayed
            Payment.objects.create(total=total, date=request.POST['date'], amountPaid=amountPaid,
                                   totalRemaining=totalRemaining,service=ser)
            return HttpResponseRedirect(redirect_to='/api/rest/payments/'+str(pk)+'/addpayments/')
    else:
        return HttpResponse('Forbidden access', status=403)
@login_required
def clientpayments(request,pk):
    ser = Service.objects.get(pk=pk)
    payments = Payment.objects.filter(service=ser)
    u = ser.user
    username = request.user.username
    if not username:
        username = None
    if payments:
        pay = payments[0]
        for paym in payments:
            if paym.date > pay.date:
                pay=paym
    else:
        payments=0
    template = get_template('clientpayments.html')
    if request.method == 'GET':
        html = template.render({'pay':pay,'ser': ser, 'u': u, 'payments': payments, 'username': username},request)
        return HttpResponse(html)
    #retrieve all users to access their services
@login_required
def clients(request):
    if request.user.is_superuser and request.user.is_staff:
        users=get_user_model().objects.filter(is_superuser=False, is_staff=False)
        username = request.user.username
        if not username:
            username = None
        template = get_template('users.html')
        if request.method == 'GET':
            html = template.render({'users':users,'username': username}, request)
            return HttpResponse(html)
    else:
        return HttpResponse('Forbidden access', status=403)
#retrieve all services to access their payments
@login_required
def usersservices(request,pk):
    if request.user.is_superuser and request.user.is_staff:
        forms = ServiceForm()
        u=get_user_model().objects.get(pk=pk)
        services = Service.objects.filter(user=u)
        username = request.user.username
        if not username:
            username = None
        if not services:
            services=None
        template = get_template('usersservices.html')
        if request.method == 'GET':
            html = template.render({'forms': forms, 'services': services,'u':u,'username': username}, request)
            return HttpResponse(html)
        elif request.method == 'POST':
            forms = ServiceForm(data=request.POST)
            if forms.is_valid():
                Service.objects.create(name=request.POST['name'], description=request.POST['description'],
                cost=request.POST['cost'],percentage= request.POST['percentage'], user=u)
                return HttpResponseRedirect(redirect_to='/api/rest/services/'+str(u.id)+'/addservices/')
            else:
                html = template.render({'forms': forms, 'services': services, 'u': u, 'username': username}, request)
                return HttpResponse(html)
    else:
        return HttpResponse('Forbidden access', status=403)

#retrieve all posts
def allposts(request):
    template = get_template('posts.html')
    allposts = Post.objects.all()
    images = Image.objects.all()
    sform = SearchForm()

    username = request.user.username
    if not username:
        username = None
    if request.method=='GET':
        html = template.render({'images':images,'allposts':allposts,'username':username,'sform':sform }, request)
        return HttpResponse(html)
    elif request.method == 'POST':
        name=request.POST['name']
        allposts = Post.objects.filter(postTitle__icontains=name)
        # filtrando con icontains no importan las mayusculas ni minusculas
        if allposts.count == 0:
            allposts = 0
        sform = SearchForm()
        html = template.render({'images': images, 'allposts':allposts, 'username': username, 'sform': sform}, request)
        return HttpResponse(html)
def contact(request):
    template = get_template('contacto.html')
    username = request.user.username
    if not username:
        username = None
    if request.method=='GET':
        html = template.render({'username':username }, request)
        return HttpResponse(html)

@login_required
def singlepost(request,pk):
    if request.user.is_superuser and request.user.is_staff:
        formp = PostForm()
        formd = DeleteService()
        username = request.user.username
        post = Post.objects.get(pk=pk)
        images = Image.objects.filter(post=post)
        if not username:
            username = None
        template = get_template('postdata.html')
        contador=0
        if request.method == 'GET':
            html = template.render({'formp': formp,'contador':contador,
            'images':images,'formd': formd, 'username': username, 'post': post},request)
            return HttpResponse(html)
        elif request.method == 'POST':
            if request.POST['delete'] == "update":
                try:
                    post.postTitle = request.POST['postTitle']
                    post.postDescription = request.POST['postDescription']
                    post.save()
                except Payment.DoesNotExist:
                    pass
                return HttpResponseRedirect(redirect_to='/api/rest/posts/' + str(pk) + '/data/')
            elif request.POST['delete'] == "delete":
                Post.objects.filter(pk=pk).delete()
                return HttpResponseRedirect(redirect_to='/api/newpost/')
            elif request.POST['delete'] == "deleteimg":
                Image.objects.filter(pk=request.POST['imgid']).delete()
                return HttpResponseRedirect(redirect_to='/api/rest/posts/' + str(pk) + '/data/')
    else:
        return HttpResponse('Forbidden access', status=403)
class Login(APIView):
    def post(self, request, format=None):
        data = request.data
        flag = data.get('flag')
        if flag == "login":
            username = data.get('usuario')
            password = data.get('password')
            account = authenticate(username=username, password=password)
            if account is not None:
                user = get_user_model().objects.get(username=username)
                if user.is_active:
                    login(request, account)
                    if user.is_superuser and user.is_staff:
                        return HttpResponseRedirect("/api/newpost/")
                    #serialized = UserSerializer(account)
                    return HttpResponseRedirect("/api/home/")
                else:
                    return HttpResponse('Bad Request', status=400)
            else:
                return HttpResponse('Bad Request', status=400)
        elif flag=="register":
            formu = SignUpForm(data=request.POST)
            #formu.fields['username'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['name'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['firstLastName'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['secondLastName'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['password'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['password2'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['email'].error_messages = {'required': 'Este campo es requerido'}
            if formu.is_valid():
                serializer = UserSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                return HttpResponseRedirect("/api/login/")
            else:
                username = request.user.username
                if not username:
                    username = None
                form = SignInForm()
                return render(request, 'login.html', {'form': form,'formu':formu,'username':username  })
        else:
            return HttpResponse('Bad Request', status=400)
    def get(self, request, format=None):
        username = request.user.username
        if not username:
            username = None
        formu = SignUpForm()
        form = SignInForm()
        return render(request, 'login.html', {'form': form,'formu':formu,'username':username  })
@login_required
def clientservices(request):
    u = request.user
    services = Service.objects.filter(user=u)
    username = u.username
    if not username:
        username = None
    if not services:
        services = None
    template = get_template('clientservices.html')
    if request.method == 'GET':
        html = template.render({'services': services, 'u': u, 'username': username}, request)
        return HttpResponse(html)
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class ResponseViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return HttpResponseRedirect("/api/login/")