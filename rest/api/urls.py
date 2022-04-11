from django.urls import path,include
from .views import articlelist,article_detail,ArticleView,ArticleDetailView,GenericApiView
urlpatterns=[
    path('article/',ArticleView.as_view(),name="article-list"),
    path('generic/detail/<int:id>/',GenericApiView.as_view(),name="generic-view"),
    path('generic/detail/',GenericApiView.as_view(),name="generic-view"),
    path('detail/<int:id>/',ArticleDetailView.as_view(),name="article-detail")
    #path('article/',articlelist,name="article-list"),
    #path('detail/<int:id>/',article_detail,name="article-detail")
]