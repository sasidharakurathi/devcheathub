import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Category, CheatSheet#, CodeSnippet

# This line is crucial. The class MUST be named 'Command' with a capital 'C'.
class Command(BaseCommand):
    help = 'Loads cheatsheets from a specified JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file to load.')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']
        self.stdout.write(f"Loading data from {json_file_path}...")

        try:
            author = User.objects.filter(is_superuser=True).first()
            if not author:
                self.stdout.write(self.style.ERROR('No superuser found. Please create one first.'))
                return

            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for item in data:
                # Category creation logic is the same...
                parent_category_name = item.get('parent_category')
                category_name = item.get('category')
                final_category = None
                if parent_category_name:
                    parent_cat, _ = Category.objects.get_or_create(name=parent_category_name, parent=None)
                    child_cat, _ = Category.objects.get_or_create(name=category_name, parent=parent_cat)
                    final_category = child_cat
                else:
                    top_level_cat, _ = Category.objects.get_or_create(name=category_name, parent=None)
                    final_category = top_level_cat

                # Update Cheatsheet creation
                cheatsheet, created = CheatSheet.objects.get_or_create(
                    title=item['title'],
                    category=final_category,
                    defaults={
                        'author': author,
                        'description': item.get('description', ''),
                        'content': item.get('content', {}) # Save the entire content block
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'  - Cheatsheet "{cheatsheet.title}" created.'))
                else:
                    # If cheatsheet exists, update its content
                    cheatsheet.content = item.get('content', {})
                    cheatsheet.save()
                    self.stdout.write(self.style.WARNING(f'  - Cheatsheet "{cheatsheet.title}" already exists. Content updated.'))

            self.stdout.write(self.style.SUCCESS('Successfully finished loading cheatsheets!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))