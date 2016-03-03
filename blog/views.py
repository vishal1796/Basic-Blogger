from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render



from .models import Post
from .forms import PostForm

def home(request):
    query_set = Post.objects.all()
    paginator = Paginator(query_set, 5)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    context = {
        'object_list': query,
        'page_request_var': page_request_var,
    }
    return render(request, "home.html",context)


def about(request):
    return render(request, 'about.html')

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None) 
    context = {
        'form': form,
    }  
    if form.is_valid():
        instance = form.save(commit = False)           ###commit false save data in memory rather in database
        instance.save()
        #messages.success(request, "Successfully Created")                                               
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, 'post_create.html', context)



def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)                                              
    context = {                                            
        'title': instance.title,                          
        'instance': instance,
    }
    if request.user.is_staff or  request.user.is_superuser:
        return render(request, "post_detail_admin.html", context)
    return render(request, "post_detail.html", context)
        
    



def post_update(request, slug = None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None, instance  = instance)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        ##
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }    
    return render(request, "post_create.html",context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    ##
    return redirect("blog:list")