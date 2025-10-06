from django.contrib import admin
from .models import Category, CheatSheet, CodeSnippet

class CodeSnippetInline(admin.StackedInline):
    model = CodeSnippet
    extra = 1
    fields = ('title', 'language', 'code', 'output')
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name' , 'slug')
    prepopulated_fields = {'slug': ('name', )}
    
@admin.register(CheatSheet)
class CheatSheetAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'updated_at')
    list_filter = ('category', )
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title', )}
    inlines = [CodeSnippetInline]
