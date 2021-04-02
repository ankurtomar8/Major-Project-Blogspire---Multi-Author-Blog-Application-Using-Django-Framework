from django.urls import path
from . import views
from .views import ( PostListView,PostDetailView,PostCreateView,
                         PostUpdateView,
                         PostDeletelView,
                         UserPostListView,
                         LikeView, 
                         PostCommentView )


urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name = 'user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete', PostDeletelView.as_view(), name = 'post-delete'), 
    path('about/', views.about, name = 'blog-about'),
    path('like/<int:pk>', LikeView, name = 'like_post'),
    path('post/<int:pk>/comment/', PostCommentView.as_view(), name = 'add_comment'),


    
]


# <app> /<model>_<viewtype>.html