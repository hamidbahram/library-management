from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from django.http import HttpResponse
from .models import BookModel
from.forms import BookForm


def index(request):
    return redirect('login')


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':  # Validate the entered data, and save
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # Add new user to customer group automatically
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            message = messages.success(
                request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:  # Authenticate user if it is Ok, go to dashboard
            login(request, user)
            return redirect('books')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


# User should be authenticated to be able to see this page
@login_required(login_url='login')
def booklist_page(request):

    items = BookModel.objects.all().order_by('-publish')

    paginator = Paginator(items, 7)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    q = request.GET.get('q')  # Search input

    if q:
        # Show similar results by user search # Using Q for multiple search
        query_set = items.filter(Q(name__icontains=q) | Q(
            author__icontains=q)).distinct()

        if not query_set:
            return redirect('books')

        elif query_set:
            paginator = Paginator(query_set, 7)

            page = request.GET.get('page')

            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            context = {
                'page': page,
                'posts': posts,
                'query':str(q),
            }
            return render(request, 'booklist.html', context)

    context = {
        'page': page,
        'posts': posts,
    }

    return render(request, 'booklist.html', context)


@login_required(login_url='login')
def add_book(request):

    if request.method == 'POST':

        form = BookForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('books')
    else:

        # Fill user and publish hidden inputs
        initial_data = {
            'user': request.user,
            'publish': timezone.now(),
        }

        form = BookForm(initial_data)
        context = {
            'form': form,
        }

        return render(request, 'add_new.html', context)


@login_required(login_url='login')
def edit_book(request, pk):
    item = get_object_or_404(BookModel, pk=pk)

    if request.method == 'POST':

        form = BookForm(request.POST, instance=item)
        if form.is_valid():

            form.save()
            return redirect('books')

    else:

        form = BookForm(instance=item)

        context = {
            'form': form,
        }

        return render(request, 'edit_item.html', context)


# User should be in admin group to be able to use delete_book method
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_book(request, pk):

    BookModel.objects.filter(id=pk).delete()

    items = BookModel.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'booklist.html', context)


# User should be in admin group to be able to see this page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def userlist_page(request):
    users_query = User.objects.all().order_by('-date_joined')

    # Get admin group users and customer group users for templates
    admin_group = Group.objects.get(name='admin')
    customer_group = Group.objects.get(name='customer')
    admins = User.objects.all().filter(groups=admin_group)
    customers = User.objects.all().filter(groups=customer_group)

    paginator = Paginator(users_query, 7)

    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'users': users,
        'admins': admins,
        'customers': customers,
    }

    return render(request, 'userlist.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_user(request, pk):

    User.objects.filter(id=pk).delete()

    return redirect('users')


# Join users to admin group
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def promote_user(request, pk):

    group_admin = Group.objects.get(name='admin')
    group_customer = Group.objects.get(name='customer')

    user = User.objects.get(id=pk)

    user.groups.add(group_admin)
    user.groups.remove(group_customer)

    return redirect('users')


# Showing user info # Reset user password via email
@login_required(login_url='login')
def user_page(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'accounts/user.html', context)