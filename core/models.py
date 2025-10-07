from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )
    order = models.PositiveIntegerField(default=0)
    icon = models.FileField(upload_to='category_icons/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class CheatSheet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="cheatsheets", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="A brief description of the cheatsheet.")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class CodeSnippet(models.Model):
    cheatsheet = models.ForeignKey(CheatSheet, related_name="snippets", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    code = models.TextField()
    output = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=50, help_text="e.g., python, bash, javascript")
    
    def __str__(self):
        return f"{self.title} for {self.cheatsheet.title}"