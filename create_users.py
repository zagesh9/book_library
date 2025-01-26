import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_library.settings')
django.setup()

from django.contrib.auth.models import User

def create_users():
    # Create staff user
    admin_username = 'admin'
    admin_password = 'admin'

    if not User.objects.filter(username=admin_username).exists():
        User.objects.create_user(
            username=admin_username,
            password=admin_password,
            is_staff=True,
            is_superuser=False
        )
        print(f"Staff user '{admin_username}' created successfully.")
    else:
        print(f"Staff user '{admin_username}' already exists.")

    # Create superuser
    superadmin_username = 'superadmin'
    superadmin_password = 'super'

    if not User.objects.filter(username=superadmin_username).exists():
        User.objects.create_superuser(
            username=superadmin_username,
            password=superadmin_password
        )
        print(f"Superuser '{superadmin_username}' created successfully.")
    else:
        print(f"Superuser '{superadmin_username}' already exists.")

if __name__ == '__main__':
    create_users()
