from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post , Comment
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django import forms

# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()  # list of dict
     }
    return render(request, 'blog/home.html' , context)

  
    
  

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    
    liked = False    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True    


    return HttpResponseRedirect(reverse ('post-detail',args=[str(pk)]))








class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app> /<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app> /<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        

     

class PostDetailView(DetailView):
    model = Post


    def get_context_data(self, *args,**kwargs):
        context = super(PostDetailView,self).get_context_data(*args,**kwargs)
        
        post_like = get_object_or_404(Post,id=self.kwargs['pk'])
        total_likes = post_like.total_likes()

        liked = False
        if post_like.likes.filter(id=self.request.user.id).exists():
            liked = True 
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context
    


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    fields = ['title','content']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeletelView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    


def about(request):
    return render(request, 'blog/about.html', {'title':'About' } )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ('name' , 'body')

        widgets ={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
        }




class PostCommentView(CreateView,CommentForm):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
        
    success_url = reverse_lazy('blog-home')
   





