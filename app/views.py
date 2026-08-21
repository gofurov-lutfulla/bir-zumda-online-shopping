import random

from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Product, UserModel
from .utils import generate_code, send_register_email


def legacy_html_redirect(request, page):
    mapping = {
        'index': 'index',
        'aloqa': 'aloqa',
        'biz-haqimizda': 'biz-haqimizda',
        'blog': 'blog',
        'mahsulotlar': 'mahsulotlar',
        'savatcha': 'savatcha',
        'checkout': 'checkout',
        'login': 'login',
        'register': 'register',
        'forgot-password': 'forgot-password',
        'reset-password': 'reset-password',
        'confirm-password': 'confirm-password',
    }

    if page == 'blog-detail':
        return redirect('blog-detail', pk=1)

    if page == 'mahsulot-detail':
        return redirect('mahsulot-detail', pk=1)

    if page in mapping:
        return redirect(mapping[page])

    return redirect('index')


def index(request):
    return render(request, 'app/index.html')


def aloqa(request):
    return render(request, 'app/aloqa.html')


def biz_haqimizda(request):
    return render(request, 'app/biz-haqimizda.html')


def blog(request):
    return render(request, 'app/blog.html')


def blog_detail(request, pk):
    context = {'pk': pk}
    return render(request, 'app/blog-detail.html', context)


def mahsulotlar(request):
    products = Product.objects.all()
    query = request.GET.get('search')

    if query:
        products = products.filter(
            Q(name__icontains=query) &
            Q(category__icontains=query)
        )

        sort_option = request.GET.get('sort')

        if sort_option == "low-price":
            products = products.order_by('price')
        elif sort_option == "high-price":
            products = products.order_by('-price')

    context = {
        'products': products,
    }

    return render(request, 'app/mahsulotlar.html', context)


def mahsulot_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app/mahsulot-detail.html', {'product': product})


def savatcha(request):
    return render(request, 'app/savatcha.html')


def checkout(request):
    return render(request, 'app/checkout.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = UserModel.objects.get(email=email)

        login(request, user)

        return redirect('index')

    return render(request, 'app/login.html')


def register_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password2')

        if int(password) != int(password1):
            return render(
                request,
                'app/register.html',
                {'errors': "Passwords didn't match"}
            )

        if UserModel.objects.filter(email=email).exists():
            return render(
                request,
                'app/register.html',
                {'errors': "Email already exists"}
            )

        user = UserModel.objects.create(
            name=name,
            email=email,
            password=password,
        )

        code = generate_code()

        request.session["verify_user_id"] = user.id
        request.session["verify_code"] = str(code)

        send_register_email(
            to_email=user.email,
            code=code
        )

        return redirect('confirm-password')

    return render(request, 'app/register.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return render(
                request,
                'app/forgot-password.html',
                {'errors': "Bunday email topilmadi"}
            )

        code = generate_code()

        request.session["reset_user_id"] = user.id
        request.session["reset_code"] = str(code)

        send_register_email(
            to_email=user.email,
            code=code
        )

        return redirect('reset-password')

    return render(request, 'app/forgot-password.html')


def reset_password(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        password = request.POST.get('password')
        password1 = request.POST.get('password2')

        if code != request.session.get("reset_code"):
            return render(
                request,
                'app/reset-password.html',
                {'errors': "Kod noto'g'ri"}
            )

        if password != password1:
            return render(
                request,
                'app/reset-password.html',
                {'errors': "Passwords didn't match"}
            )

        user = UserModel.objects.get(
            id=request.session.get("reset_user_id")
        )

        user.password = password
        user.save()

        request.session.pop("reset_code", None)
        request.session.pop("reset_user_id", None)

        return redirect('login')

    return render(request, 'app/reset-password.html')


def confirm_password(request):
    if request.method == 'POST':
        if request.POST.get('code') == request.session.get("verify_code"):

            user = UserModel.objects.get(
                id=request.session.get("verify_user_id")
            )

            user.is_active = True
            user.save()

            request.session.pop("verify_code", None)
            request.session.pop("verify_user_id", None)

            return redirect('login')

    return render(request, 'app/confirm-password.html')