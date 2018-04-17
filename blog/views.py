from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, render_to_response
from django.shortcuts import redirect
from .forms import PostForm
from .models import Document
from .forms import DocumentForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
  
    return render(request, 'blog/post_list.html', {'posts':posts})



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})



def post_new(request):
    # form = PostForm()
    # return render(request, 'blog/post_edit.html', {'form': form})



    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


# def display_songs(request, pk):
# 	songs = get_object_or_404(Song, pk=pk)
# 	return render(request, 'blog/songs.html', {'songs': songs})


def image_list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(request , 
        'blog/list.html',
        {'documents': documents, 'form': form}
      
    )
