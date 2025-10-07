import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Category, CheatSheet, CodeSnippet

# This line is crucial. The class MUST be named 'Command' with a capital 'C'.
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
                self.stdout.write(self.style.ERROR('No superuser found. Please create one first with "python manage.py createsuperuser"'))
                return

            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for item in data:
                category, created = Category.objects.get_or_create(name=item['category'])
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Category "{category.name}" created.'))
                
                cheatsheet, created = CheatSheet.objects.get_or_create(
                    title=item['title'],
                    author=author,
                    category=category,
                    defaults={'description': item['description']}
                )

                if created:
                    for snippet_data in item['snippets']:
                        CodeSnippet.objects.create(
                            cheatsheet=cheatsheet,
                            title=snippet_data['title'],
                            language=snippet_data['language'],
                            code=snippet_data['code'],
                            output=snippet_data.get('output', None)
                        )
                    self.stdout.write(f'  - Cheatsheet "{cheatsheet.title}" created.')
                else:
                    self.stdout.write(self.style.WARNING(f'  - Cheatsheet "{cheatsheet.title}" already exists. Skipping.'))

            self.stdout.write(self.style.SUCCESS('Successfully finished loading cheatsheets!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{json_file_path}" not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))