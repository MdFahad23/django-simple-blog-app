from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import (
    View,
    TemplateView,
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid

from App_Blog.models import Blog, Comment, Like
from App_Blog.forms import CommentForm

# Create your views here.


class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = "App_Blog/My_blog.html"


class Blog_List(ListView):
    context_object_name = "blogs"
    model = Blog
    template_name = "App_Blog/Blog_list.html"
    # queryset = Blog.objects.order_by("-publish_date")


class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = "App_Blog/Create_blog.html"
    fields = ("blog_title", "blog_content", "blog_image")

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()

        return HttpResponseRedirect(reverse("index"))


@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()

    already_liked = Like.objects.filter(blog=blog, user=request.user)

    if already_liked:
        liked = True
    else:
        liked = False

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(
                reverse("App_Blog:blog_details", kwargs={"slug": slug})
            )

    return render(
        request,
        "App_Blog/Blog_details.html",
        context={"blog": blog, "comment_form": comment_form, "liked": liked},
    )


@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user

    already_liked = Like.objects.filter(blog=blog, user=user)

    if not already_liked:
        like_post = Like(blog=blog, user=user)
        like_post.save()
    return HttpResponseRedirect(
        reverse("App_Blog:blog_details", kwargs={"slug": blog.slug})
    )


@login_required
def unLiked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(
        reverse("App_Blog:blog_details", kwargs={"slug": blog.slug})
    )


class EditBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ("blog_title", "blog_content", "blog_image")
    template_name = "App_Blog/Edit_blog.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy("App_Blog:blog_details", kwargs={"slug": self.object.slug})
