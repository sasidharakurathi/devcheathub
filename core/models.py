from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
import random
import string

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
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
        unique_together = ('parent', 'name')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            # Check if a category with this slug already exists
            while Category.objects.filter(slug=slug).exists():
                # If it exists, append a random 4-character string
                random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
                slug = f'{base_slug}-{random_string}'
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class CheatSheet(models.Model):
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="cheatsheets", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="A brief description of the cheatsheet.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    content = models.JSONField(default=dict)
    
    def get_sections_and_tags(self):
        """
        Parses the JSON content to extract main sections and all associated tags.
        Returns:
            {'sections': [{'title': 'Section 1', 'subsections': [{'heading': 'sub1', 'tags': ['t1']}]}], 'all_tags': ['t1', 't2']}
        """
        sections = []
        all_tags = set() # Use a set to automatically handle unique tags

        if isinstance(self.content, dict) and 'sections' in self.content:
            for section in self.content.get('sections', []):
                section_data = {
                    'title': section.get('section_title'),
                    'subsections': []
                }
                for subsection in section.get('sub_sections', []):
                    # Extract tags directly from the subsection
                    current_tags = subsection.get('tags', [])
                    section_data['subsections'].append({
                        'heading': subsection.get('sub_section_heading'),
                        'tags': current_tags
                    })
                    all_tags.update(current_tags) # Add all tags to our set

                sections.append(section_data)
        
        # Also include any tags directly associated with the cheatsheet model (if you have them)
        # For now, we rely solely on JSON content for tags.
        
        return {'sections': sections, 'all_tags': sorted(list(all_tags))} # Return sorted list of unique tags

    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            # Check if a cheatsheet with this slug already exists
            while CheatSheet.objects.filter(slug=slug).exists():
                # If it exists, append a random 4-character string
                random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
                slug = f'{base_slug}-{random_string}'
            self.slug = slug
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('cheatsheet_detail', kwargs={'cheatsheet_slug': self.slug})

    
    def __str__(self):
        return self.title

# class CodeSnippet(models.Model):
#     cheatsheet = models.ForeignKey(CheatSheet, related_name="snippets", on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     code = models.TextField()
#     output = models.TextField(null=True, blank=True)
#     language = models.CharField(max_length=50, help_text="e.g., python, bash, javascript")
    
#     def __str__(self):
#         return f"{self.title} for {self.cheatsheet.title}"