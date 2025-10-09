from django.contrib import admin
from .models import Category, CheatSheet, CodeSnippet

@admin.action(description='Approve selected cheatsheets')
def make_approved(modeladmin, request, queryset):
    queryset.update(status='APPROVED')

class CodeSnippetInline(admin.StackedInline):
    model = CodeSnippet
    extra = 1
    fields = ('title', 'language', 'code', 'output')
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order', 'slug')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'parent', 'order', 'icon')
    
@admin.register(CheatSheet)
class CheatSheetAdmin(admin.ModelAdmin):
    list_display = ('author','title', 'category','status', 'updated_at')
    list_filter = ('category', )
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title', )}
    inlines = [CodeSnippetInline]
    actions = [make_approved]
