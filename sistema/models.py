from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class AbstractModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateField(auto_now_add=True)
    class Meta:
        abstract = True
        ordering = ['-createdAt']

    def __str__(self):
        return (self.id)

class Post (AbstractModel):
    postTitle = models.CharField(max_length=50, null=False, blank=False)
    postDescription = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField()
    def __str__(self):
        return self.postTitle

class Comment (AbstractModel):
    createdBy = models.CharField(max_length=50, null=False, blank=False)
    text = models.CharField(max_length=500, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.text

class Response (AbstractModel):
    repliedBy = models.CharField(max_length=50, null=True, blank=True)
    text = models.CharField(max_length=500, null=False, blank=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    def __str__(self):
        return self.text
#
class User(AbstractBaseUser):
    username = models.CharField(max_length=20, null=False, blank=False, unique=True)
    #password = models.CharField(max_length=30, null=False, blank=False) clashes with the AbstractBaseUser field
    is_active = models.BooleanField(default=True)#este campo es necesario
    is_staff = models.BooleanField(default=False)#este campo es necesario
    is_superuser = models.BooleanField(default=False)#este campo es necesario
    fullName = models.CharField(max_length=70)
    #     type = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fullName']
    def __str__(self):
          return self.username

class Service (AbstractModel):
     name = models.CharField(max_length=30, null=False, blank=False)
     description = models.CharField(max_length=200, null=False, blank=False)
     cost = models.FloatField(null=False, blank=False)
     percentage = models.IntegerField(null=True, blank=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     def __str__(self):
         return self.name

class Payment (AbstractModel):
     date = models.DateField(null=False, blank=False)
     total = models.FloatField(null=False, blank=False)
     amountPaid = models.FloatField(null=False, blank=False)
     totalRemaining = models.FloatField(null=False, blank=False)
     service = models.ForeignKey(Service, on_delete=models.CASCADE)
     def __str__(self):
         return self.service
