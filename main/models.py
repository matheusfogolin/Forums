from django.db import models
from tinymce.models import HTMLField
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
from registration.models import User
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length = 50)
    slug = models.SlugField(max_length = 450, unique = True, blank = True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)      
        super(Category, self).save(*args, **kwargs)
        
    def get_url(self):
        return reverse("posts", kwargs = {
            "slug": self.slug,
        })
        
    @property
    def post_count(self):
        return Post.objects.filter(categories=self).count()
        
    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest("date")
    
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.content[:100]
    
    class Meta:
        verbose_name_plural = "replies"  

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    replies = models.ManyToManyField(Reply, blank = True)
    
    def __str__(self):
        return self.content[:100]

class Post(models.Model):
    title = models.CharField('Título do post', max_length = 450)
    slug = models.SlugField(max_length = 450, unique = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = HTMLField('Conteúdo')
    categories = models.ManyToManyField(Category, verbose_name = 'Categorias')
    date = models.DateTimeField(auto_now_add = True)
    approved = models.BooleanField(default = True)
    hit_count_generic = GenericRelation(HitCount, object_id_field = 'object_pk', related_query_name = 'hit_count_generic_relation')
    comments = models.ManyToManyField(Comment, blank = True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)      
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse("detail", kwargs={
            "slug":self.slug
        })
    
    @property
    def comments_count(self):
        return self.comments.count()
    
    @property
    def last_reply(self):
        return self.comments.latest("date")