from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Movie, Director
from .forms import MovieForm, DirectorForm
from store.models import Product
from store.forms import ProductForm


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel:dashboard')

    error = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect(request.POST.get('next') or 'admin_panel:dashboard')
        error = True

    return render(request, 'admin_panel/login.html', {'error': error})


@staff_member_required(login_url='/admin-panel/login/')
def dashboard(request):
    return render(request, 'admin_panel/dashboard.html', {
        'total_movies': Movie.objects.count(),
        'total_directors': Director.objects.count(),
        'total_products': Product.objects.count(),
        'recent_movies': Movie.objects.order_by('-created_at')[:5],
        'recent_products': Product.objects.order_by('-created_at')[:5],
    })


# ===== Movies =====

@staff_member_required(login_url='/admin-panel/login/')
def movies_list(request):
    movies = Movie.objects.select_related('director').order_by('-created_at')
    return render(request, 'admin_panel/movies_list.html', {'movies': movies})


@staff_member_required(login_url='/admin-panel/login/')
def movies_create(request):
    form = MovieForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'เพิ่มหนังสำเร็จ!')
        return redirect('admin_panel:movies_list')
    return render(request, 'admin_panel/movies_form.html', {
        'form': form,
        'action': 'เพิ่ม',
        'directors': Director.objects.all(),
    })


@staff_member_required(login_url='/admin-panel/login/')
def movies_edit(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = MovieForm(request.POST or None, request.FILES or None, instance=movie)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'แก้ไขหนังสำเร็จ!')
        return redirect('admin_panel:movies_list')
    return render(request, 'admin_panel/movies_form.html', {
        'form': form,
        'action': 'แก้ไข',
        'directors': Director.objects.all(),
        'current_image': movie.poster_image if movie.poster_image else None,
    })


@staff_member_required(login_url='/admin-panel/login/')
def movies_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'ลบหนังสำเร็จ!')
        return redirect('admin_panel:movies_list')
    return render(request, 'admin_panel/movies_delete.html', {'movie': movie})


# ===== Directors =====

@staff_member_required(login_url='/admin-panel/login/')
def directors_list(request):
    directors = Director.objects.all()
    return render(request, 'admin_panel/directors_list.html', {'directors': directors})


@staff_member_required(login_url='/admin-panel/login/')
def directors_create(request):
    form = DirectorForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'เพิ่มผู้กำกับสำเร็จ!')
        return redirect('admin_panel:directors_list')
    return render(request, 'admin_panel/directors_form.html', {'form': form, 'action': 'เพิ่ม'})


@staff_member_required(login_url='/admin-panel/login/')
def directors_edit(request, pk):
    director = get_object_or_404(Director, pk=pk)
    form = DirectorForm(request.POST or None, request.FILES or None, instance=director)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'แก้ไขผู้กำกับสำเร็จ!')
        return redirect('admin_panel:directors_list')
    return render(request, 'admin_panel/directors_form.html', {
        'form': form,
        'action': 'แก้ไข',
        'current_image': director.profile_image if director.profile_image else None,
    })


@staff_member_required(login_url='/admin-panel/login/')
def directors_delete(request, pk):
    director = get_object_or_404(Director, pk=pk)
    if request.method == 'POST':
        director.delete()
        messages.success(request, 'ลบผู้กำกับสำเร็จ!')
        return redirect('admin_panel:directors_list')
    return render(request, 'admin_panel/directors_delete.html', {'director': director})


# ===== Products =====

@staff_member_required(login_url='/admin-panel/login/')
def products_list(request):
    products = Product.objects.order_by('-created_at')
    return render(request, 'admin_panel/products_list.html', {'products': products})


@staff_member_required(login_url='/admin-panel/login/')
def products_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'เพิ่มสินค้าสำเร็จ!')
        return redirect('admin_panel:products_list')
    return render(request, 'admin_panel/products_form.html', {'form': form, 'action': 'เพิ่ม'})


@staff_member_required(login_url='/admin-panel/login/')
def products_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'แก้ไขสินค้าสำเร็จ!')
        return redirect('admin_panel:products_list')
    return render(request, 'admin_panel/products_form.html', {
        'form': form,
        'action': 'แก้ไข',
        'current_image': product.image if product.image else None,
    })


@staff_member_required(login_url='/admin-panel/login/')
def products_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'ลบสินค้าสำเร็จ!')
        return redirect('admin_panel:products_list')
    return render(request, 'admin_panel/products_delete.html', {'product': product})
