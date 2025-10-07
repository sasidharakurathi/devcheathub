import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Category, CheatSheet, CodeSnippet

class Command(BaseCommand):
    help = 'Loads cheatsheets from a specified JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file to load.')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']
        
        self.stdout.write(f"Loading data from {json_file_path}...")

        try:
            # Get the first superuser to be the author of all cheatsheets
            author = User.objects.filter(is_superuser=True).first()
            if not author:
                self.stdout.write(self.style.ERROR('No superuser found. Please create one first.'))
                return

            with open(json_file_path, 'r') as f:
                data = json.load(f)

            for item in data:
                # Get or create the category
                category, created = Category.objects.get_or_create(name=item['category'])
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Category "{category.name}" created.'))
                
                # Create the CheatSheet
                cheatsheet = CheatSheet.objects.create(
                    author=author,
                    category=category,
                    title=item['title'],
                    description=item['description']
                )

                # Create the associated CodeSnippets
                for snippet_data in item['snippets']:
                    CodeSnippet.objects.create(
                        cheatsheet=cheatsheet,
                        title=snippet_data['title'],
                        language=snippet_data['language'],
                        code=snippet_data['code'],
                        output=snippet_data.get('output', None) # Safely get output
                    )
                
                self.stdout.write(f'  - Cheatsheet "{cheatsheet.title}" created.')

            self.stdout.write(self.style.SUCCESS('Successfully loaded all cheatsheets!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{json_file_path}" not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))