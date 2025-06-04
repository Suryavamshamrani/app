# Setup Django environment first
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')
django.setup()

# Now import Django models
from django.contrib.auth.models import User
from userauth.models import Community, CommunityMembership
import uuid

def add_users_to_community():
    # Get the community ID from user input
    print("Available communities:")
    communities = Community.objects.all()
    
    if not communities.exists():
        print("No communities found. Please create a community first.")
        return
    
    # List all communities
    for idx, community in enumerate(communities, 1):
        member_count = CommunityMembership.objects.filter(community=community).count()
        print(f"{idx}. {community.name} - Members: {member_count}/5")
    
    try:
        choice = int(input("\nEnter the number of the community you want to add users to: "))
        selected_community = communities[choice-1]
    except (ValueError, IndexError):
        print("Invalid selection. Please try again.")
        return
    
    # Check if community already has 5 members
    current_member_count = CommunityMembership.objects.filter(community=selected_community).count()
    if current_member_count >= 5:
        print(f"This community already has {current_member_count} members and has reached the maximum limit of 5.")
        return
    
    # Get available users who are not already members
    existing_member_ids = CommunityMembership.objects.filter(
        community=selected_community
    ).values_list('user_id', flat=True)
    
    available_users = User.objects.exclude(id__in=existing_member_ids)
    
    if not available_users.exists():
        print("No available users to add to this community.")
        return
    
    # List available users
    print("\nAvailable users:")
    for idx, user in enumerate(available_users, 1):
        print(f"{idx}. {user.username}")
    
    # Get user selections
    slots_available = 5 - current_member_count
    max_to_add = min(2, slots_available)  # Limit to 2 users or available slots
    
    print(f"\nYou can add up to {max_to_add} users to this community.")
    
    selected_users = []
    for i in range(max_to_add):
        try:
            choice = int(input(f"Enter the number for user {i+1} (or 0 to stop): "))
            if choice == 0:
                break
            selected_user = available_users[choice-1]
            selected_users.append(selected_user)
        except (ValueError, IndexError):
            print("Invalid selection. Skipping this user.")
    
    # Add selected users to the community
    for user in selected_users:
        CommunityMembership.objects.create(
            user=user,
            community=selected_community
        )
        print(f"Added {user.username} to {selected_community.name}")
    
    print(f"\nCommunity {selected_community.name} now has {current_member_count + len(selected_users)}/5 members.")

if __name__ == "__main__":
    # This will only run when the script is executed directly
    add_users_to_community()
