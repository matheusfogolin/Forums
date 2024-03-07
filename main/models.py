from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
from registration.models import User

class Author(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    first_name = models.CharField('Nome', max_length = 30)
    last_name = models.CharField('Sobrenome', max_length = 30)
    slug = models.SlugField(max_length = 450, unique = True, blank = True)
    bio = HTMLField()
    points = models.IntegerField(default = 0)
    profile_pic = ResizedImageField(size=[50, 80], quality = 100, upload_to = "authors", null = True, default = None, blank = True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}' 
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.first_name} {self.last_name}')
        super(Author, self).save(*args, **kwargs)
        
    @property
    def num_posts(self):
        return Post.objects.filter(user=self).count()
    
    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

class Category(models.Model):
    title = models.CharField(max_length = 50)
    slug = models.SlugField(max_length = 450, unique = True, blank = True)
    
    class Meta:
        verbose_name_plural = "categories"
    
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
    user = models.ForeignKey(Author, on_delete = models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.content[:100]
    
    class Meta:
        verbose_name_plural = "replies"  

class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete = models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    replies = models.ManyToManyField(Reply, blank = True)
    
    def __str__(self):
        return self.content[:100]

class Post(models.Model):
    title = models.CharField('Título do post', max_length = 450)
    slug = models.SlugField(max_length = 450, unique = True, blank = True)
    user = models.ForeignKey(Author, on_delete = models.CASCADE)
    content = HTMLField('Conteúdo')
    categories = models.ManyToManyField(Category)
    date = models.DateTimeField(auto_now_add = True)
    approved = models.BooleanField(default = False)
    hit_count_generic = GenericRelation(HitCount, object_id_field = 'object_pk', related_query_name = 'hit_count_generic_relation')
    tags = TaggableManager()
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