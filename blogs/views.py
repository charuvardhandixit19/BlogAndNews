
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer
import requests
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout as auth_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser


# News API key
NEWS_API_KEY = '007f40311f70499592675e680d054bf3'

def home(request):
    if request.user.is_authenticated:
        return render(request, 'blogs/home.html', {'logged_in': True})
    else:
        return render(request, 'blogs/home.html', {'logged_in': False})

from .forms import PasswordResetForm

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            
            # Get the user object based on the username
            user = User.objects.get(username=username)
            
            # Set the new password and save the user
            user.set_password(new_password)
            user.save()
            
            # Optionally, log the user in automatically after resetting the password
            update_session_auth_hash(request, user)  # Keep the user logged in after password change

            # Provide feedback to the user
            messages.success(request, "Your password has been reset successfully.")
            return redirect('login')  # Redirect to the login page or wherever appropriate
            
    else:
        form = PasswordResetForm()

    return render(request, 'blogs/password_reset.html', {'form': form})

# User Authentication Views
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blogs/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('news_home')
    else:
        form = AuthenticationForm()
    return render(request, 'blogs/login.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

# News Views
@login_required
def news_home(request):
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    news = response.json().get('articles', [])
    return render(request, 'blogs/news_home.html', {'news': news})

# Blog Views
@login_required
def blog_dashboard(request):
    blogs = Blog.objects.filter(author=request.user)
    return render(request, 'blogs/blog_dashboard.html', {'blogs': blogs})

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Blog.objects.create(title=title, content=content, author=request.user)
        return redirect('blog_dashboard')
    return render(request, 'blogs/create_blog.html')


@login_required
def delete_blog(request, blog_id):
    if request.method == 'POST':  # Only allow POST requests for deletion
        blog = get_object_or_404(Blog, id=blog_id, author=request.user)
        blog.delete()
        return redirect('blog_dashboard')
    return HttpResponseForbidden("You are not allowed to delete this blog.")

    


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])  # Restrict to admin users
def admin_blog_api(request):
    if request.method == 'GET':
        # Fetch all blogs
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Create a new blog
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # Update an existing blog (requires 'id' in request data)
        blog_id = request.data.get('id')  # Get blog ID from request data
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete a specific blog (requires 'id' in request data)
        blog_id = request.data.get('id')
        if blog_id:
            try:
                blog = Blog.objects.get(id=blog_id)
                blog.delete()
                return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_200_OK)
            except Blog.DoesNotExist:
                return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If no ID is provided, delete all blogs (optional)
            Blog.objects.all().delete()
            return Response({'message': 'All blogs deleted successfully'}, status=status.HTTP_200_OK)
