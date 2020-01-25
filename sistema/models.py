import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
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

class CustomUserManager(BaseUserManager):
    def create_user(self, username, name,firstLastName,secondLastName, email, password=None):
        if not username:
            raise ValueError('Llena el campo de tu nombre de usuario')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name ,firstLastName=firstLastName, secondLastName=secondLastName)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name,firstLastName,secondLastName, email, password=None):
        if not username:
            raise ValueError('Llena el campo de tu nombre de usuario')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, firstLastName=firstLastName, secondLastName=secondLastName)
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=20, null=False, blank=False, unique=True)
    # password = models.CharField(max_length=30, null=False, blank=False) clashes with the AbstractBaseUser field
    is_active = models.BooleanField(default=True)  # este campo es necesario
    is_admin = models.BooleanField(default=False)  # este campo es necesario
    name = models.CharField(max_length=50, blank=False, null=False)
    firstLastName = models.CharField(max_length=50, blank=False, null=False)
    secondLastName = models.CharField(max_length=50, blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=False, blank=False)
    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','firstLastName','secondLastName','email']
    def get_full_name(self):
        full_name=self.name+self.firstLastName+self.secondLastName
        return full_name
    def get_short_name(self):
        return self.name
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
#has_perm(perm, obj=None): aquí me quede en la documentación
#Returns True if the user has the named permission. If obj is provided, the permission needs to be checked against a specific object instance.
class Service (AbstractModel):
     name = models.CharField(max_length=30, null=False, blank=False)
     description = models.CharField(max_length=200, null=False, blank=False)
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

