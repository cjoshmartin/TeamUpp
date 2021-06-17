from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'teamupp'

urlpatterns = [
    path('', views.HomeView.as_view(), name="index"),

    # user/teammate Views
    path('invite/', views.InviteUserView.as_view(), name='invite'),
    path(
        'invite/success/',
        TemplateView.as_view(
            template_name="teamupp/invite_user/success.html"),
        name='invite-success'
    ),
    path(
        'user/<int:pk>',
        views.UserDetailView.as_view(),
        name="user-details"
         ),

    # Project Views
    path('project/create/', views.CreateProjectView.as_view(), name="create-project"),
    path(
        'project/success/',
        TemplateView.as_view(
            template_name="teamupp/create_project/success.html"),
        name='project-success'
    ),
    path(
        'project/<int:pk>/',
        views.ProjectDetailView.as_view(),
        name="project-details"
    ),

    # Groups
    path(
        'group/<int:pk>/',
        views.GroupsDetailView.as_view(),
        name="group-details"
    ),

    # Search
    path(
        'search/',
        views.SearchResultsView.as_view(),
        name="search"
    ),

    #  User Accounts
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegisterUserView.as_view(), name="register"),
    path(
        'accounts/register/success',
        TemplateView.as_view(template_name='registration/register/success.html'),
        name="register-success"
    ),

    # Company
    path(
        'company/<int:pk>',
        views.CompanyDetailView.as_view(),
        name="company-details"
         )

]
