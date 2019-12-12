from django.db import models
import uuid


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