from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('projects/', views.list_project, name='list_project'),
    path('projects/new/', views.create_project, name='create_project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.update_project, name='update_project'),
    path('projects/<int:pk>/delete', views.delete_project, name='delete_project'),
    path('projects/<int:project_pk>/tasks/new/', views.create_todo_task, name='create_todo_task'),
    path('projects/<int:project_pk>/tasks/<int:todo_task_pk>/edit/', views.update_todo_task, name='update_todo_task'),
    path('projects/<int:project_pk>/tasks/<int:todo_task_pk>/delete/', views.delete_todo_task, name='delete_todo_task'),
    path('projects/<int:project_pk>/tasks/<int:todo_task_pk>/vote/', views.todo_task_vote, name='todo_task_vote'),
    path('projects/<int:project_pk>/tasks/<int:todo_task_pk>/suggest/', views.todo_task_suggest, name='todo_task_suggest'),
    path('projects/<int:project_id>/invite/', views.invite_your_team, name='invite_your_team'),
    path('projects/invite/<str:token>/', views.accept_invite, name='accept_invite'),
]