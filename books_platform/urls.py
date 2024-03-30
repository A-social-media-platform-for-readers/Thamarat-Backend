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
from django.urls import path, include

from users.views import *
from books.views import *

from rest_framework.routers import DefaultRouter


BookRouter = DefaultRouter()
BookRouter.register(r"books", BookViewSet)

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
    path("auth/login/", LoginView.as_view()),
    path("auth/user/", UserView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    # book end points
    path("", include(BookRouter.urls)),
    path(
        "books-pagination-filter-genre/<str:genre>/",
        BookPaginationFilterGenre.as_view({"get": "list"}),
    ),
    path(
        "books-pagination-filter-genre-price/<str:genre>/<int:min_value>/<int:max_value>/<str:order_from>/",
        BookPaginationFilterGenreAndPrice.as_view({"get": "list"}),
    ),
    path(
        "books-pagination-free-books/",
        BookPaginationFreeBooks.as_view({"get": "list"}),
    ),
    path(
        "books-pagination-high-rate/",
        BookPaginationHighRateBooks.as_view({"get": "list"}),
    ),
    path(
        "books-pagination-popular-books/",
        BookPaginationPopularBooks.as_view({"get": "list"}),
    ),
    path("books/review/<int:pk>/", BookReview.as_view({"get": "retrieve"})),
    path("books/search/<str:string>/", BookSearch.as_view({"get": "list"})),
]
