from rest_framework.parsers import JSONParser

from .forms import *
from django.http import HttpResponse
from django.template.loader import get_template
from sistema.serializers import *
from rest_framework import generics, permissions
from rest_framework import viewsets
# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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
            if request.method == 'GET':
                html = template.render({'img': img,'comment': comment, 'form':form, 'formr':formr }, request)
                return HttpResponse(html)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    if request.method=='GET':
        html = template.render({'img': img, 'comment':comment, 'form':form, 'formr':formr }, request)
        return HttpResponse(html)

    elif request.method == 'POST':
        if request.POST['respuesta']:
            try:
                com=Comment.objects.get(pk=request.POST['primarkey'])
            except Comment.DoesNotExist:
                com=0
            formr = ResponseForm(data=request.POST)
            formr.fields['respuesta'].error_messages = {'required': 'Este campo es requerido'}
            if formr.is_valid():
                Response.objects.create(text=request.POST['respuesta'], comment=com)
            comment = Comment.objects.filter(post=img)
            html = template.render({'img': img, 'comment': comment, 'form': form, 'formr': formr}, request)
            return HttpResponse(html)
        elif  request.POST['mensaje'] and request.POST['usuario']:
            form = ContactForm(data=request.POST)
            form.fields['mensaje'].error_messages = {'required': 'Este campo es requerido'}
            form.fields['usuario'].error_messages = {'required': 'Este campo es requerido'}
            if form.is_valid():
                Comment.objects.create(createdBy=request.POST['usuario'], text=request.POST['mensaje'], post=img)
            comment = Comment.objects.filter(post=img)
            html = template.render({'img': img, 'comment': comment, 'form': form, 'formr':formr}, request)
            return HttpResponse(html)

class ResponseViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer