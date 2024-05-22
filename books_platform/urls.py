"""
URL configuration for books_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.urls import path, include

from users.views import *
from books.views import *
from social_media.views import *

# from rest_framework.routers import DefaultRouter


# BookRouter = DefaultRouter()
# BookRouter.register(r"books", BookViewSet)

urlpatterns = [
    # admin end point
    path("admin/", admin.site.urls),
    # API auto documentation end points
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # User authentication end points
    path("auth/register/", RegisterView.as_view({"post": "create"})),
    path("auth/login/", LoginView.as_view({"post": "login"})),
    path("auth/logout/", LogoutView.as_view({"post": "logout"})),
    path("auth/user/", UserView.as_view({"get": "retrieve"})),
    path(
        "auth/user/<int:pk>/",
        UserViewSet.as_view({"get": "retrieve", "put": "update"}),
    ),
    # book end points
    # path("", include(BookRouter.urls)),
    path("books/", BookViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "books/<int:pk>/",
        BookViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path("books/review/<int:pk>/", BookReview.as_view({"get": "retrieve"})),
    path("books/search/<str:string>/", BookSearch.as_view({"get": "list"})),
    path(
        "books/filter-genre/<str:genre>/",
        BookFilterGenre.as_view({"get": "list"}),
    ),
    path(
        "books/filter-genre-price/<str:genre>/<int:min_value>/<int:max_value>/<str:order_from>/",
        BookFilterGenreAndPrice.as_view({"get": "list"}),
    ),
    path(
        "books/free-books/",
        FreeBooks.as_view({"get": "list"}),
    ),
    path(
        "books/high-rate/",
        HigherRatingBooks.as_view({"get": "list"}),
    ),
    path(
        "books/popular-books/",
        PopularBooks.as_view({"get": "list"}),
    ),
    # book summary end points
    path(
        "books-summary/create/<int:book_id>/",
        BookSummaryCreate.as_view({"post": "create"}),
    ),
    path(
        "books-summary/list/<int:book_id>/",
        BookSummaryList.as_view({"get": "list"}),
    ),
    path(
        "books-summary/<int:book_id>/<int:summary_id>/",
        BookSummaryUdateDelete.as_view({"put": "update", "delete": "destroy"}),
    ),
    # social media end points
    # Post end points
    path(
        "social-media/posts/",
        PostViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "social-media/posts/<int:pk>/",
        PostViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path(
        "social-media/posts/likes-counter/<int:pk>/",
        PostLikeViewSet.as_view({"post": "like", "delete": "unlike"}),
    ),
    # Comment end points
    path(
        "social-media/comments/<int:post_id>/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "social-media/comments/<int:comment_id>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        "social-media/comments/likes-counter/<int:comment_id>/",
        CommentLikeViewSet.as_view({"post": "like", "delete": "unlike"}),
    ),
    # InnerComment end points
    path(
        "social-media/inner-comments/<int:comment_id>/",
        InnerCommentViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "social-media/inner-comments/<int:inner_comment_id>/",
        InnerCommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        "social-media/inner-comments/likes-counter/<int:inner_comment_id>/",
        InnerCommentLikeViewSet.as_view({"post": "like", "delete": "unlike"}),
    ),
]

urlpatterns += staticfiles_urlpatterns()
