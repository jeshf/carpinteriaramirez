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


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

# desplegar una imagen en el archivo imagen.html
def image(request,pk):
    form = ContactForm()
    formr = ResponseForm()
    template = get_template('image.html')
    try:
        img = Post.objects.get(pk=pk)
        try:
            comment = Comment.objects.filter(post=img)
        except Comment.DoesNotExist:
            comment = 0
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    if request.method=='GET':
        html = template.render({'img': img, 'comment':comment, 'form':form, 'formr':formr }, request)
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
                Response.objects.create(text=request.POST['respuesta'], comment=com)
            formr= ResponseForm()
            html = template.render({'img': img, 'comment': comment, 'form': form, 'formr': formr}, request)
            return HttpResponse(html)
        elif  request.POST['flag']=="comentar":
            form = ContactForm(data=request.POST)
            form.fields['mensaje'].error_messages = {'required': 'Este campo es requerido'}
            form.fields['usuario'].error_messages = {'required': 'Este campo es requerido'}
            if form.is_valid():
                Comment.objects.create(createdBy=request.POST['usuario'], text=request.POST['mensaje'], post=img)
            comment = Comment.objects.filter(post=img)
            form= ContactForm()
            html = template.render({'img': img, 'comment': comment, 'form': form, 'formr':formr}, request)
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
                    return render(request, 'profile.html', {'object': serialized.data})
                else:
                    return HttpResponse('Unauthorized', status=401)
            else:
                return HttpResponse('Unauthorized', status=401)
        elif flag=="register":
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return render(request, 'profile.html', {'object': serializer.data})
        else:
            return HttpResponse('Bad Request', status=400)
    def get(self, request, format=None):
        formu = SignUpForm()
        form = SignInForm()
        return render(request, 'login.html', {'form': form,'formu':formu})

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