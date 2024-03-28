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
# from books.routers import router

urlpatterns = [
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
    path("admin/", admin.site.urls),
    path("api/register", RegisterView.as_view({"post": "create"})),
    path("api/login", LoginView.as_view()),
    path("api/user", UserView.as_view()),
    path("api/logout", LogoutView.as_view()),

    # path("", include(router.urls)),
    path("api/create_book", CreateBook.as_view({"post": "create"})),
    path("api/all_books", ListAllBooks.as_view()),
    path("api/get_books", BookViewSet.as_view({"get": "list"})),
    path("api/get_book/<int:pk>", RetrieveBook.as_view()),
    path("api/filter_books/<str:genre>", BookFilter.as_view({"get": "list"})),
    path("api/update_book/<int:pk>", UpdateBook.as_view()),
    path("api/delete_book/<int:pk>", DeleteBook.as_view()),
    path("api/review_book/<int:pk>", ReviewBook.as_view()),
    path("api/search_books", BookSearchView.as_view()),
]
