from django.urls import path
from .views import LoginAPIView, LogoutAPIView, DocumentListAPIView, DocUpdateDeleteAPIView, MyProfileAPIView

urlpatterns = [
    #################  USER ###############################
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("my-profile/", MyProfileAPIView.as_view(), name="logout"),



    ##################   DOC ###########################
    path("docs/list/", DocumentListAPIView.as_view(), name="logout"),
    path('docs/delete/', DocUpdateDeleteAPIView.as_view(), name='docs-delete'),
    path('docs/update/<int:pk>/', DocUpdateDeleteAPIView.as_view(), name='docs-update'),
]