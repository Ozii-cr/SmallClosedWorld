#!/usr/bin/env python
import os
import shutil
import subprocess
import sys
from dotenv import load_dotenv

def create_env_file():
    """Create .env file from example if it doesn't exist."""
    if not os.path.exists('.env') and os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("Created .env file from .env.example")
    else:
        print(".env file already exists or .env.example not found")

def setup_database():
    """Run database migrations."""
    # Load environment variables
    load_dotenv()
    
    environment = os.getenv('ENVIRONMENT', 'development')
    if environment == 'production':
        print("Setting up PostgreSQL for production...")
        # Additional production setup could go here
    else:
        print("Setting up SQLite for development...")
    
    # Run migrations
    subprocess.run([sys.executable, 'manage.py', 'makemigrations'])
    subprocess.run([sys.executable, 'manage.py', 'migrate'])

def create_superuser():
    """Create a superuser if one doesn't exist."""
    from django.contrib.auth.models import User
    if not User.objects.filter(is_superuser=True).exists():
        username = input("Enter superuser username: ")
        email = input("Enter superuser email: ")
        from django.db.utils import IntegrityError
        
        while True:
            try:
                User.objects.create_superuser(username, email, input("Enter superuser password: "))
                print(f"Superuser {username} created successfully.")
                break
            except IntegrityError:
                print("User with that username already exists. Try another one.")
                username = input("Enter another superuser username: ")
    else:
        print("Superuser already exists.")

if __name__ == "__main__":
    # Make sure Django settings are loaded
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
    
    # Create .env file if it doesn't exist
    create_env_file()
    
    # Setup database based on environment
    setup_database()
    
    # Ask if user wants to create a superuser
    if input("Do you want to create a superuser? (y/n): ").lower() == 'y':
        # We need to setup Django before creating a superuser
        import django
        django.setup()
        create_superuser()
    
    print("\nSetup complete! You can now run the application.")
    print("Development: python manage.py runserver")
    print("Start Celery: celery -A project_name worker -l info")