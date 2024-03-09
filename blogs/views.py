from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from blogs.models import Blog, Category

def posts_by_category(request, category_id):
    posts=Blog.objects.filter(status='published', category=category_id)
    try:
        categori=Category.objects.get(id=category_id)
    except:
        return redirect('home')
    # the above try-except block is to redirect user to homepage if there are no posts available for specific category we can also use get_object_or_404 to get 404 error page
    #categori=get_object_or_404(Category,id=category_id)
    context={
        'posts':posts,
        'categori':categori
    }
    return render(request,'posts_by_category.html', context)
