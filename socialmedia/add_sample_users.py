# Setup Django environment first
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')
django.setup()

# Now import Django models
from django.contrib.auth.models import User
from userauth.models import Profile, Post
from django.core.files.images import ImageFile
from django.conf import settings

def create_sample_users():
    # Sample user data
    sample_users = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'samplepass123',
            'bio': 'Photography enthusiast and nature lover',
            'location': 'New York'
        },
        {
            'username': 'sarah_smith',
            'email': 'sarah@example.com',
            'password': 'samplepass123',
            'bio': 'Travel blogger and food critic',
            'location': 'Los Angeles'
        },
        {
            'username': 'mike_johnson',
            'email': 'mike@example.com',
            'password': 'samplepass123',
            'bio': 'Software developer and tech enthusiast',
            'location': 'San Francisco'
        },
        {
            'username': 'emily_wilson',
            'email': 'emily@example.com',
            'password': 'samplepass123',
            'bio': 'Fitness trainer and wellness coach',
            'location': 'Chicago'
        },
        {
            'username': 'alex_brown',
            'email': 'alex@example.com',
            'password': 'samplepass123',
            'bio': 'Digital artist and graphic designer',
            'location': 'Seattle'
        }
    ]
    
    created_users = []
    
    # Create users and profiles
    for user_data in sample_users:
        # Check if user already exists
        if not User.objects.filter(username=user_data['username']).exists():
            # Create user
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            
            # Create profile
            profile = Profile.objects.create(
                user=user,
                id_user=user.id,
                bio=user_data['bio'],
                location=user_data['location']
            )
            
            print(f"Created user: {user.username}")
            created_users.append(user)
        else:
            print(f"User {user_data['username']} already exists")
    
    return created_users

if __name__ == "__main__":
    # This will only run when the script is executed directly
    create_sample_users()
    print("Sample users created successfully!")