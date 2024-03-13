from django.shortcuts import get_object_or_404, redirect, render
from .forms import BlogpostForm, CategoryForm
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

@login_required(login_url='login')
def dashboard(request):
    category_count=Category.objects.all().count()
    blog_count= Blog.objects.all().count()
    context={
        'category_count':category_count,
        'blog_count':blog_count,
    }
    return render(request, 'dashboard/dashboard.html',context)

def categories(request):
    return render(request, 'dashboard/categories.html')

def add_category(request):
    if request.method =='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form=CategoryForm()
    context={
        'form':form,
    }
    return render(request, 'dashboard/categories_add.html', context)

def edit_category(request, pk):
    category= get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form=CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category,
    }
    return render(request, 'dashboard/edit_category.html', context)

def delete_category(request, pk):
    category= get_object_or_404(Category,pk=pk)
    category.delete()
    return redirect('categories')

def posts(request):
    post=Blog.objects.all()
    context={
        'post':post,
    }
    return render(request, 'dashboard/posts.html', context)

def add_posts(request):
    if request.method == 'POST':
        form=BlogpostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author= request.user
            post.save()
            title=form.cleaned_data['title']
            post.slug= slugify(title)+ '-' + str(post.id)
            post.save()
            return redirect('posts')
        else:
            print(form.errors)
    form=BlogpostForm()
    context={
        'form':form,
    }
    return render(request, 'dashboard/add_posts.html', context)

def edit_posts(request, pk):
    post=get_object_or_404(Blog, pk=pk)
    if request.method =='POST':
        form=BlogpostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post=form.save()
            title=form.cleaned_data['title']
            post.slug=slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')

    form=BlogpostForm(instance=post)
    context={
        'form':form,
        'post':post,
    }
    return render(request, 'dashboard/edit_post.html', context)

def delete_posts(request, pk):
    post= get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')