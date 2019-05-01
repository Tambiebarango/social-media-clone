from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (TemplateView, ListView,DetailView,
                                    CreateView, UpdateView,DeleteView,)
from django.contrib.auth.mixins import LoginRequiredMixin
from blogapp.forms import PostForm, CommentForm, Userform
from blogapp.models import Post, Comment
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blogapp/post_detail.html'

    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blogapp/post_detail.html'

    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = '/'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)










@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST) #pass in what they filled into the form
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blogapp/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    return redirect('post_detail', pk = post_pk)

def index(request):
    return render(request, 'blogapp/post_list.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request,'blogapp/post_list.html')

def signup(request):

    registered = False


    if request.method == "POST":
        user_form = Userform(data=request.POST)


        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)

    else:
            user_form = Userform()
    return render(request, 'blogapp/signup.html',
                            {'Userform': user_form,
                            'registered': registered})


def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return render(request,'blogapp/post_list.html')
                # return render(request, '/')
            else:
                return HttpResponse("Account is not active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,'blogapp/login.html',{})
