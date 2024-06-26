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

from AI.views import *
from users.views import *
from books.views import *
from social_media.views import *

from django.urls import converters
from django.urls import register_converter


class FloatUrlParameterConverter:
    """Custom converter to ensure float type"""

    regex = r"[0-9]+\.?[0-9]*"  # Match any float or integer number

    def to_python(self, value):
        try:
            return float(value)
        except ValueError:
            raise converters(value, message="Invalid float parameter")


register_converter(FloatUrlParameterConverter, "float&integer")

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
    # User end points
    path("users/", UserViewSet.as_view({"get": "list"})),
    path(
        "users/<int:pk>/",
        UserViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path(
        "users/follow/<int:user_to_followed_id>/",
        FollowView.as_view({"post": "follow"}),
    ),
    path(
        "users/unfollow/<int:user_to_unfollowed_id>/",
        FollowView.as_view({"delete": "unfollow"}),
    ),
    path("users/followers/<int:user_id>/", FollowView.as_view({"get": "followers"})),
    path("users/following/<int:user_id>/", FollowView.as_view({"get": "following"})),
    path("users/search/<str:string>/", UserSearch.as_view({"get": "list"})),
    # AI end points
    path(
        "AI/OCR/<int:book_id>/<int:start_page>/<int:end_page>/<str:language>/",
        OCR.as_view({"post": "pdf2text"}),
    ),
    path(
        "AI/translation/<str:text>/<str:language>/",
        Translate.as_view({"post": "translate"}),
    ),
    # book end points
    # path("", include(BookRouter.urls)),
    path("books/user-list/<int:user_id>/", BookUserList.as_view({"get": "list"})),
    path("books/6", BookViewSet6.as_view({"get": "list"})),
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
    path(
        "books/<int:book_id>/download/",
        BookDownload.as_view({"get": "download_book_pdf"}),
    ),
    path(
        "books/<int:book_id>/cover-image/download/",
        BookCoverDownload.as_view({"get": "download_book_cover"}),
    ),
    path(
        "books/rate/<int:book_id>/<float&integer:rating>/",
        BookRate.as_view({"post": "rate"}),
    ),
    path(
        "books/readed/<int:book_id>/",
        WantToRead.as_view({"post": "readed"}),
    ),
    path(
        "books/reading/<int:book_id>/",
        WantToRead.as_view({"post": "reading"}),
    ),
    path(
        "books/to-read/<int:book_id>/",
        WantToRead.as_view({"post": "want_to_read"}),
    ),
    path(
        "books/readed/",
        WantToRead.as_view({"get": "get_readed_books"}),
    ),
    path(
        "books/reading/",
        WantToRead.as_view({"get": "get_reading_books"}),
    ),
    path(
        "books/to-read/",
        WantToRead.as_view({"get": "get_to_read_books"}),
    ),
    path(
        "books/delete-readed/<int:book_id>/",
        WantToRead.as_view({"delete": "delete_readed_book"}),
    ),
    path(
        "books/delete-reading/<int:book_id>/",
        WantToRead.as_view({"delete": "delete_reading_book"}),
    ),
    path(
        "books/delete-to-read/<int:book_id>/",
        WantToRead.as_view({"delete": "delete_to_read_book"}),
    ),
    path(
        "books/reviews/<int:book_id>/",
        BookReviewView.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "books/review/<int:Review_id>/<int:book_id>/",
        BookReviewView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        "books/review/<int:Review_id>/likes/",
        BookReviewLikes.as_view({"post": "like", "delete": "unlike"}),
    ),
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
        "books-summary/<int:summary_id>/",
        BookSummaryUdateDelete.as_view({"put": "update", "delete": "destroy"}),
    ),
    path(
        "books-summary/<int:book_summary_id>/download/",
        BookSummaryDownload.as_view({"get": "download_book_summary_pdf"}),
    ),
    # social media end points
    # Post end points
    path(
        "social-media/posts/user-list/<int:user_id>/",
        PostUserList.as_view({"get": "list"}),
    ),
    path("social-media/posts/create/", PostCreate.as_view({"post": "create"})),
    path(
        "social-media/posts/",
        PostViewSet.as_view({"get": "list"}),
    ),
    path(
        "social-media/posts/<int:post_id>/",
        PostViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path(
        "social-media/posts/<int:post_id>/likes/",
        PostLikeViewSet.as_view({"post": "like", "delete": "unlike"}),
    ),
    # Comment end points
    path(
        "social-media/posts/comments/create/",
        CommentCreate.as_view({"post": "create"}),
    ),
    path(
        "social-media/posts/comments/<int:post_id>/",
        CommentViewSet.as_view({"get": "list"}),
    ),
    path(
        "social-media/posts/comment/<int:comment_id>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        "social-media/posts/comments/<int:comment_id>/likes/",
        CommentLikeViewSet.as_view({"post": "like", "delete": "unlike"}),
    ),
    # InnerComment end points
    path(
        "social-media/posts/comments/inner-comments/create/",
        InnerCommentCreate.as_view({"post": "create"}),
    ),
    path(
        "social-media/posts/comments/inner-comments/<int:comment_id>/",
        InnerCommentViewSet.as_view({"get": "list"}),
    ),
    path(
        "social-media/posts/comments/inner-comment/<int:inner_comment_id>/",
        InnerCommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        "social-media/posts/comments/inner-comments/<int:inner_comment_id>/likes/",
        InnerCommentLikeViewSet.as_view({"post": "like", "delete": "unlike"}),
    ),
    # Chat end points
    path("chat/create/", MessageCreate.as_view({"post": "create"})),
    path("chat/", MessageViewSet.as_view({"get": "list"})),
    path(
        "chat/<int:message_id>/",
        MessageViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]

urlpatterns += staticfiles_urlpatterns()
