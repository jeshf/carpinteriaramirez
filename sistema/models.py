import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from carpinteriaramirez import settings
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
    def __str__(self):
        return self.postTitle

class Comment (AbstractModel):
    createdBy = models.CharField(max_length=20, null=False, blank=False)
    text = models.CharField(max_length=500, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.text

class Image (AbstractModel):
    imagePath = models.ImageField(null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.imagePath

class Response (AbstractModel):
    repliedBy = models.CharField(max_length=20, null=True, blank=True)
    text = models.CharField(max_length=500, null=False, blank=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    def __str__(self):
        return self.text

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username, name,firstLastName,secondLastName, email, password):
        if not username:
            raise ValueError('Llena el campo de tu nombre de usuario')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name ,firstLastName=firstLastName, secondLastName=secondLastName)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name,firstLastName,secondLastName, email, password):
        if not username:
            raise ValueError('Llena el campo de tu nombre de usuario')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name, firstLastName=firstLastName, secondLastName=secondLastName)
        user.is_staff = True
        user.is_superuser =True
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=20, null=False, blank=False, unique=True)
    # password = models.CharField(max_length=30, null=False, blank=False) clashes with the AbstractBaseUser field
    is_active = models.BooleanField(default=True)  # este campo es necesario
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # este campo es necesario
    name = models.CharField(max_length=50, blank=False, null=False)
    firstLastName = models.CharField(max_length=50, blank=False, null=False)
    secondLastName = models.CharField(max_length=50, blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','firstLastName','secondLastName','email']
    #def get_full_name(self):
        #full_name=self.name+self.firstLastName+self.secondLastName
        #return full_name
    #def get_short_name(self):
        #return self.name
    def __str__(self):
        return self.username

    #def has_perm(self, perm, obj=None):
        #"Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        #return True

    #def has_module_perms(self, app_label):
        #"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        #return True

    #@property
    #def is_superuser(self):
        #return self.superuser

    #@property
    #def is_active(self):
        #return self.active

    #@property
    #def is_staff(self):
        #return self.is_staff
class Service (AbstractModel):
     name = models.CharField(max_length=50, null=False, blank=False)
     description = models.CharField(max_length=500, null=False, blank=False)
     cost = models.FloatField(null=False, blank=False)
     percentage = models.IntegerField(null=True, blank=True)
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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

