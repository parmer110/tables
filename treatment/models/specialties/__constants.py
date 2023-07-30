# constants.py

import os
from django.apps import apps
from importlib import import_module

# Get the app config for the 'treatment' app
treatment_app_config = apps.get_app_config('treatment')

# Get the path to the 'models' module inside the 'treatment' app
models_module_path = os.path.join(treatment_app_config.path, 'models')

# Get the names of sub-packages inside the 'models' module
spec_packages = [name for name in os.listdir(models_module_path) if os.path.isdir(os.path.join(models_module_path, name)) and not name.startswith('__')]

# Use 'spec_packages' to create the choices for the form field
choices1 = [(package, package) for package in spec_packages]

choices2 = []
spec_module_path = 'treatment.models.specialties'
spec_module = import_module(spec_module_path)
spec_files = os.listdir(os.path.dirname(spec_module.__file__))
for spec_file in spec_files:
    if spec_file.endswith('.py') and not spec_file.startswith('__'):
        spec_module_name = os.path.splitext(spec_file)[0]
        spec_module = import_module(f'{spec_module_path}.{spec_module_name}')
        choices2.append((spec_module.name, spec_module_name))

choices3 = []
spec_module_path = 'treatment.models.specialties'
spec_module = import_module(spec_module_path)
spec_files = os.listdir(os.path.dirname(spec_module.__file__))
for spec_file in spec_files:
    if spec_file.endswith('.py') and not spec_file.startswith('__'):
        spec_module_name = os.path.splitext(spec_file)[0]
        spec_module = import_module(f'{spec_module_path}.{spec_module_name}')
        choices3.append((getattr(spec_module, 'name'), getattr(spec_module, 'name')))
