from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm #might not need this
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Project, Todo_Task, InviteToProject
from .forms import ProjectForm, Todo_TaskForm, CustomUserCreationForm
from django.utils.crypto import get_random_string
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import JsonResponse

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm();
    
    return render(request, 'registration/signup.html', {'form': form})


def home(request):
    return render(request, 'projects_page/home.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'registration/profile.html', {'user': user})

#handles showing all the projects created by the logged in user
@login_required
def list_project(request): 
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'projects_page/list_project.html', {'projects': projects})

#handles creating a new project 
@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid(): 
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('list_project')
    else:
        form = ProjectForm()
    return render(request, 'projects_page/project_form.html', {'form': form})    

#show a specific projects page 
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    # currently working on a sidbar functionality by combining detail and list pages 
    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     return render(request, 'projects_page/partial_detail.html', {'project': project})
    return render(request, 'projects_page/project_detail.html', {'project': project})

# updating an exisiting project file
@login_required
def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if project.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects_page/project_form.html', {'form': form})

# delete
@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if project.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        project.delete()
        return redirect('list_project')
    return redirect('list_project')

        

# now for tasks 
@login_required
def create_todo_task(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, owner=request.user)
    if request.method == 'POST':
        form = Todo_TaskForm(request.POST)
        if form.is_valid():
            todo_task = form.save(commit=False)
            todo_task.project = project
            todo_task.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = Todo_TaskForm()
    return render(request, 'projects_page/todo_task_form.html', {'form': form, 'project': project})

@login_required
def update_todo_task(request, project_pk, todo_task_pk):
    project = get_object_or_404(Project, pk=project_pk, owner=request.user)
    todo_task = get_object_or_404(Todo_Task, pk=todo_task_pk, project=project)
    if request.method == 'POST':
        form = Todo_TaskForm(request.POST, instance=todo_task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project_pk)
    else:
        form = Todo_TaskForm(instance=todo_task)
    return render(request, 'projects_page/todo_task_form.html', {'form': form, 'project': project})

@login_required
def delete_todo_task(request, project_pk, todo_task_pk):
    project = get_object_or_404(Project, pk=project_pk, owner=request.user)
    todo_task = get_object_or_404(Todo_Task, pk=todo_task_pk, project=project)
    if request.method == 'POST':
        todo_task.delete()
        return redirect('project_detail', pk=project.pk)
    return render(request, 'projects_page/todo_task_delete.html', {'todo_task': todo_task, 'project': project})


# view for team voting 
def todo_task_vote(request, project_pk, todo_task_pk):
    project = get_object_or_404(Project, pk=project_pk, owner=request.user)
    todo_task = get_object_or_404(Todo_Task, pk=todo_task_pk, project=project)
    todo_task.votes += 1
    todo_task.save()
    return redirect('project_detail', pk=project_pk)

#view for handing team suggestions inside the project detail
def todo_task_suggest(request, project_pk, todo_task_pk):
    project = get_object_or_404(Project, pk=project_pk, owner=request.user)
    todo_task = get_object_or_404(Todo_Task, pk=todo_task_pk, project=project)
    if request.method == 'POST':
        suggestion = request.POST.get('suggestion')
        todo_task.suggestions += f'{suggestion}\n'
        todo_task.save()
    return redirect('project_detail', pk=project.pk)

# this will handle sending an invitation link and also generating a token and sending that token to the team memeber
def invite_your_team(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        email = request.POST['email']
        token = get_random_string(32)
        invite = InviteToProject.objects.create(email=email, project=project, token=token)
        invite_url_relative = reverse('accept_invite', args=[token])
        invite_url_absolute = f'https://{request.get_host()}{invite_url_relative}'
        send_mail(
            'You have been invited to join your team project',
            f'Follow the link to join the project: {invite_url_absolute}',
            'dont-reply@procrastinaut.com',
            [email],
            fail_silently=False,
        )
        return redirect('project_detail', pk=project_id)
    return render(request, 'invitations/invite.html', {'project': project})

# so when a user invites their team to the project,
# first I want to check if they already have an account, if not - I should ask them to create an account
# after they create an account, they should be accepted and be added as the projects team member
def accept_invite(request, token):
    invite = get_object_or_404(InviteToProject, token=token)
    if invite.is_expired() or invite.is_accepted:
        return render(request, 'invitations/invite_expired.html')
    
    if request.user.is_authenticated:
        invite.project.team_members.add(request.user)
        invite.is_accepted = True
        invite.save()
        return redirect('project_detail', project_id=invite.project.id)
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            invite.project.team_members.add(user)
            invite.is_accepted = True
            invite.save()
            return redirect('project_detail', project_id=invite.project.id)
            #once the user logs in, they can access the project
    else: 
        form = CustomUserCreationForm()
    return render(request, 'invitations/signup_n_accept.html', {'form': form})