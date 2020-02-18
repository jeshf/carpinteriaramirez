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
    replies = 0
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
    if request.method=='GET':
        html = template.render({'img': img, 'post': post, 'comment':comment, 'form':form, 'formr':formr,
                                'replies':replies,'formar':formar,'username':username }, request)
        return HttpResponse(html)

    elif request.method == 'POST':
        if request.POST['flag']=="responder":
            try:
                com=Comment.objects.get(pk=request.POST['primarkey'])
            except Comment.DoesNotExist:
                com=0
            formr = ResponseForm(data=request.POST)
            formr.fields['respuesta'].error_messages = {'required': 'Este campo es requerido'}
            if formr.is_valid():
                usr=request.user.username
                if (not request.user.username):
                    usr="Anónimo"
                Response.objects.create(repliedBy=usr, text=request.POST['respuesta'], comment=com)
            formr= ResponseForm()
            replies = 0
            html = template.render({'img': img,'post': post, 'comment': comment, 'form': form, 'formr': formr,
                                    'replies':replies,'formar':formar,'username':username}, request)
            return HttpResponse(html)
        elif  request.POST['flag']=="comentar":
            form = ContactForm(data=request.POST)
            form.fields['mensaje'].error_messages = {'required': 'Este campo es requerido'}
            if form.is_valid():
                usr = request.user.username
                if (not request.user.username):
                    usr = "Anónimo"
                Comment.objects.create(createdBy=usr, text=request.POST['mensaje'], post=post)
            comment = Comment.objects.filter(post=post)
            form= ContactForm()
            replies = 0
            html = template.render({'img': img,'post': post, 'comment': comment, 'form': form, 'formr':formr,
                                    'replies':replies,'formar':formar,'username':username}, request)
            return HttpResponse(html)
        elif  request.POST['flag']=="respuestas":
            com=Comment.objects.get(id=request.POST['commentid'])
            replies=Response.objects.filter(comment=com)
            formar = CommentRepliesForm()
            html = template.render({'img': img,'post': post, 'comment': comment, 'form': form, 'formr':formr,
                                    'formar':formar,'username':username, 'replies':replies}, request)
            return HttpResponse(html)
def addimages(request,pk):
    formi = ImageForm()
    template = get_template('addimages.html')
    username = request.user.username
    if not username:
        username = None
    try:
        post = Post.objects.get(pk=pk)
        try:
            img = Image.objects.filter(post=post)
        except Image.DoesNotExist:
            img = 0
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    if request.method=='GET':
        html = template.render({'img': img, 'post': post, 'formi':formi,'username':username }, request)
        return HttpResponse(html)
    elif request.method == 'POST':
        imagePath=request.FILES['imagePath']
        posturl="/api/rest/posts/"+str(request.POST['postid'])+"/"
        data = {'imagePath': imagePath,'post': posturl}
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return HttpResponse('Bad Request', status=400)
        return HttpResponseRedirect("/api/rest/posts/" + str(post.id) + "/addimages/")
def home(request):
    template = get_template('home.html')
    img=Image.objects.all()[0:8]
    username = request.user.username
    if not username:
        username = None
    if request.method=='GET':
        html = template.render({'img': img, 'username':username}, request)
        return HttpResponse(html)
#create a new post
def post(request):
    formp = PostForm()
    allposts = Post.objects.all()
    username = request.user.username
    if not username:
        username = None
    template = get_template('createpost.html')
    if request.method=='GET':
        html = template.render({'formp':formp,'allposts':allposts,'username':username}, request)
        return HttpResponse(html)
#retrieve all posts
def allposts(request):
    template = get_template('posts.html')
    allposts = Post.objects.all()
    username = request.user.username
    if not username:
        username = None
    if request.method=='GET':
        html = template.render({'allposts':allposts,'username':username }, request)
        return HttpResponse(html)
#retrieve all comments
def allcomments(request):
    template = get_template('comments.html')
    allcomments = Comment.objects.all()
    if request.method=='GET':
        html = template.render({'allcomments':allcomments }, request)
        return HttpResponse(html)
#retrieve all services
def allservices(request):
    template = get_template('services.html')
    allservices = Service.objects.all()
    if request.method=='GET':
        html = template.render({'allservices':allservices }, request)
        return HttpResponse(html)
#retrieve all payments
def allpayments(request):
    template = get_template('payments.html')
    allpayments = Payment.objects.all()
    if request.method == 'GET':
        html = template.render({'allpayments': allpayments}, request)
        return HttpResponse(html)

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
                    serialized = UserSerializer(account)
                    return HttpResponseRedirect("/api/home/")
                else:
                    return HttpResponse('Bad Request', status=400)
            else:
                return HttpResponse('Bad Request', status=400)
        elif flag=="register":
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return HttpResponseRedirect("/api/home/")
        else:
            return HttpResponse('Bad Request', status=400)
    def get(self, request, format=None):
        username = request.user.username
        if not username:
            username = None
        formu = SignUpForm()
        form = SignInForm()
        return render(request, 'login.html', {'form': form,'formu':formu,'username':username  })

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