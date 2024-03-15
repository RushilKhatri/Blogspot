from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from blogs.models import Blog, Category, Comment
from django.db.models import Q

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

def blogs(request, slug):
    single_blog= get_object_or_404(Blog, slug=slug, status='published')
    if request.method == 'POST':
        comment=Comment()
        comment.user=request.user
        comment.blog=single_blog
        comment.comment= request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)
    comments= Comment.objects.filter(blog=single_blog)
    comm_count=comments.count()
    context={
        'single_blog':single_blog,
        'comments':comments,
        'comm_count':comm_count,
    }
    return render(request, 'blog.html', context)

def search(request):
    keyword=request.GET.get('keyword')
    blogs=Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword), status='published')
    context={
        'blogs':blogs,
        'keyword':keyword,
    }
    return render(request, 'search.html', context)