from django.urls import path
from .views import (
    LoginAPIView, LogoutAPIView, DocumentListAPIView,
    DocUpdateDeleteAPIView, MyProfileAPIView, WordDataImportAPIView,
    CategoryUpdateAPIView, CategoryDeleteAPIView, CategoryCreateAPIView
)

urlpatterns = [
    #################  USER ###############################
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("my-profile/", MyProfileAPIView.as_view(), name="logout"),



    ##################   DOC ###########################
    path("docs/json-upload/", WordDataImportAPIView.as_view(), name="logout"),
    path("docs/list/", DocumentListAPIView.as_view(), name="logout"),
    path('docs/', DocUpdateDeleteAPIView.as_view(), name='docs-delete'),
    path('docs/<int:pk>/', DocUpdateDeleteAPIView.as_view(), name='docs-update'),

    ####################  CATEGORY  ##################################
    path('category/create/', CategoryCreateAPIView.as_view()),
    path('category/update/<int:pk>/', CategoryUpdateAPIView.as_view()),
    path('category/delete/<int:pk>/', CategoryDeleteAPIView.as_view()),
]
