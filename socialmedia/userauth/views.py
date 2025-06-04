from itertools import chain
from  django . shortcuts  import  get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import  Followers, LikePost, Post, Profile
from django.db.models import Q
from django.contrib import messages
from .models import Community, CommunityMembership, CommunityPost




def signup(request):
 try:
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('emailid')
        pwd=request.POST.get('pwd')
        print(fnm,emailid,pwd)
        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        user_model = User.objects.get(username=fnm)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        if my_user is not None:
            login(request,my_user)
            return redirect('/')
        return redirect('/loginn')
    
        
 except:
        invalid="User already exists"
        return render(request, 'signup.html',{'invalid':invalid})
  
    
 return render(request, 'signup.html')
        
     
        
        
        
        
    

def loginn(request):
 
  if request.method == 'POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm,pwd)
        userr=authenticate(request,username=fnm,password=pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/')
        
 
        invalid="Invalid Credentials"
        return render(request, 'loginn.html',{'invalid':invalid})
               
  return render(request, 'loginn.html')

@login_required(login_url='/loginn')
def logoutt(request):
    logout(request)
    return redirect('/loginn')



# Add this to your imports at the top if not already there
from django.db.models import Count

# Modify your home view to include suggested users
@login_required(login_url='/loginn')
def home(request):
    
    following_users = Followers.objects.filter(follower=request.user.username).values_list('user', flat=True)

    
    post = Post.objects.filter(Q(user=request.user.username) | Q(user__in=following_users)).order_by('-created_at')

    profile = Profile.objects.get(user=request.user)
    
    # Get suggested users (users not followed by current user)
    # Exclude the current user and users already followed
    suggested_users = User.objects.exclude(username=request.user.username)\
                                  .exclude(username__in=following_users)\
                                  .order_by('?')[:5]  # Random 5 users
    
    # Get profiles for suggested users
    suggested_profiles = Profile.objects.filter(user__in=suggested_users)

    context = {
        'post': post,
        'profile': profile,
        'suggested_profiles': suggested_profiles,
    }
    return render(request, 'main.html', context)
    


@login_required(login_url='/loginn')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/loginn')
def likes(request, id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id)

        like_filter = LikePost.objects.filter(post_id=id, username=username).first()

        if like_filter is None:
            new_like = LikePost.objects.create(post_id=id, username=username)
            post.no_of_likes = post.no_of_likes + 1
        else:
            like_filter.delete()
            post.no_of_likes = post.no_of_likes - 1

        post.save()

        # Generate the URL for the current post's detail page
        print(post.id)

        # Redirect back to the post's detail page
        return redirect('/#'+id)
    
@login_required(login_url='/loginn')
def explore(request):
    post=Post.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user=request.user)

    context={
        'post':post,
        'profile':profile
        
    }
    return render(request, 'explore.html',context)
    
@login_required(login_url='/loginn')
def profile(request,id_user):
    user_object = User.objects.get(username=id_user)
    print(user_object)
    profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=id_user).order_by('-created_at')
    user_post_length = len(user_posts)

    follower = request.user.username
    user = id_user
    
    if Followers.objects.filter(follower=follower, user=user).first():
        follow_unfollow = 'Unfollow'
    else:
        follow_unfollow = 'Follow'

    user_followers = len(Followers.objects.filter(user=id_user))
    user_following = len(Followers.objects.filter(follower=id_user))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'profile': profile,
        'follow_unfollow':follow_unfollow,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    
    
    if request.user.username == id_user:
        if request.method == 'POST':
            if request.FILES.get('image') == None:
             image = user_profile.profileimg
             bio = request.POST['bio']
             location = request.POST['location']

             user_profile.profileimg = image
             user_profile.bio = bio
             user_profile.location = location
             user_profile.save()
            if request.FILES.get('image') != None:
             image = request.FILES.get('image')
             bio = request.POST['bio']
             location = request.POST['location']

             user_profile.profileimg = image
             user_profile.bio = bio
             user_profile.location = location
             user_profile.save()
            

            return redirect('/profile/'+id_user)
        else:
            return render(request, 'profile.html', context)
    return render(request, 'profile.html', context)

@login_required(login_url='/loginn')
def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()

    return redirect('/profile/'+ request.user.username)


@login_required(login_url='/loginn')
def search_results(request):
    query = request.GET.get('q')

    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)

    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'search_user.html', context)

def home_post(request,id):
    post=Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    context={
        'post':post,
        'profile':profile
    }
    return render(request, 'main.html',context)



def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')



# Add these imports at the top if not already there
from django.contrib import messages
from .models import Community, CommunityMembership, CommunityPost

# Add these new view functions

@login_required(login_url='/loginn')
def communities_list(request):
    # Get communities the user is a member of
    user_communities = Community.objects.filter(
        communitymembership__user=request.user
    )
    
    # Get all public communities
    all_communities = Community.objects.filter(is_private=False)
    
    profile = Profile.objects.get(user=request.user)
    
    context = {
        'user_communities': user_communities,
        'all_communities': all_communities,
        'profile': profile
    }
    
    return render(request, 'communities.html', context)

@login_required(login_url='/loginn')
def community_detail(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    
    # Check if user is a member of this community
    is_member = CommunityMembership.objects.filter(
        user=request.user,
        community=community
    ).exists()
    
    # If private and not a member, redirect
    if community.is_private and not is_member:
        messages.error(request, "This is a private community. You need to be a member to view it.")
        return redirect('communities_list')
    
    # Get community posts
    posts = CommunityPost.objects.filter(community=community).order_by('-created_at')
    
    # Check if user is admin
    is_admin = False
    if is_member:
        is_admin = CommunityMembership.objects.get(
            user=request.user,
            community=community
        ).is_admin
    
    # Get members
    members = CommunityMembership.objects.filter(community=community)
    
    profile = Profile.objects.get(user=request.user)
    
    context = {
        'community': community,
        'posts': posts,
        'is_member': is_member,
        'is_admin': is_admin,
        'members': members,
        'profile': profile
    }
    
    return render(request, 'community_detail.html', context)

@login_required(login_url='/loginn')
def create_community(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_private = request.POST.get('is_private') == 'on'
        banner_img = request.FILES.get('banner_img')
        
        # Create community
        community = Community.objects.create(
            name=name,
            description=description,
            created_by=request.user,
            is_private=is_private
        )
        
        if banner_img:
            community.banner_img = banner_img
            community.save()
        
        # Add creator as admin member
        CommunityMembership.objects.create(
            user=request.user,
            community=community,
            is_admin=True
        )
        
        return redirect('community_detail', community_id=community.id)
    
    profile = Profile.objects.get(user=request.user)
    return render(request, 'create_community.html', {'profile': profile})

@login_required(login_url='/loginn')
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    
    # Check if already a member
    if CommunityMembership.objects.filter(user=request.user, community=community).exists():
        messages.info(request, "You are already a member of this community.")
    else:
        # Check if community already has 5 members
        current_member_count = CommunityMembership.objects.filter(community=community).count()
        if current_member_count >= 5:
            messages.error(request, "This community has reached the maximum limit of 5 members.")
        else:
            CommunityMembership.objects.create(
                user=request.user,
                community=community
            )
            messages.success(request, f"You have joined {community.name}!")
    
    return redirect('community_detail', community_id=community.id)

@login_required(login_url='/loginn')
def leave_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    
    # Check if a member
    membership = CommunityMembership.objects.filter(
        user=request.user,
        community=community
    ).first()
    
    if membership:
        # Don't allow the creator to leave
        if community.created_by == request.user:
            messages.error(request, "As the creator, you cannot leave this community.")
        else:
            membership.delete()
            messages.success(request, f"You have left {community.name}.")
    else:
        messages.error(request, "You are not a member of this community.")
    
    return redirect('communities_list')

@login_required(login_url='/loginn')
def create_community_post(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    
    # Check if user is a member
    if not CommunityMembership.objects.filter(user=request.user, community=community).exists():
        messages.error(request, "You need to be a member to post in this community.")
        return redirect('community_detail', community_id=community.id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        post = CommunityPost.objects.create(
            user=request.user,
            community=community,
            content=content
        )
        
        if image:
            post.image = image
            post.save()
        
        messages.success(request, "Post created successfully!")
        return redirect('community_detail', community_id=community.id)
    
    profile = Profile.objects.get(user=request.user)
    return render(request, 'create_community_post.html', {
        'community': community,
        'profile': profile
    })