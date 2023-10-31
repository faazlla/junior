import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'junior.settings')
django.setup()

from website.models import Language

languages = [
    'Python', 'JavaScript', 'Java', 'C#', 'C++', 'Ruby', 'Swift', 'Kotlin', 'TypeScript', 'PHP',
    'HTML', 'CSS', 'R', 'Go', 'Scala', 'Perl', 'Lua', 'Haskell', 'Rust', 'Dart',
    'Objective-C', 'SQL', 'Shell', 'Matlab', 'Groovy', 'VHDL', 'Verilog', 'Assembly', 'F#',
]


for language_name in languages:
    language, created = Language.objects.get_or_create(name=language_name)
    if created:
        print(f'Dodat jezik: {language_name}')
    else:
        print(f'Jezik "{language_name}" već postoji u bazi podataka.')
