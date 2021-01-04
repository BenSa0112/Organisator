from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.core.paginator import Paginator
from .models import Post
from datetime import datetime, date
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    context = {
        'posts': Post.objects.all(),
    }


    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    login_required = True
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            return HttpResponse('The user is not superuser!')
        else:
            form.instance.author = self.request.user
            return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == 'test':
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def get_date_size(y):

    date_for_weekday = y.replace("-"," ")
    numbers = [int(word) for word in date_for_weekday.split() if word.isdigit()]
    date_for_weekday = date(numbers[0], numbers[1], numbers[2])

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    dt = now.strptime(dt_string,"%Y-%m-%d %H:%M:%S")

    ExpectedDate1 = str(y)
    if date_for_weekday.weekday() == 2:
        ExpectedTime2 = "21:00"
    if date_for_weekday.weekday() == 6:
        ExpectedTime2 = "11:00"
    space = " "
    ExpectedDate = ExpectedDate1 + space + ExpectedTime2
    ExpectedDate = datetime.strptime(ExpectedDate, "%Y-%m-%d %H:%M")

    if dt > ExpectedDate:
        return 0
    else:
        return 1