from django.shortcuts import render
from product.models import Product
from product.models import Comment

# Create your views here.

def home(request):
    recent_product = Product.objects.order_by('-pk')[:3]
    return render(request, 'homepage/home.html', {
        'recent_products' : recent_product,
    })

def mypage(request):
    recent_comment = Comment.objects.order_by('-pk')[:4]
    return render(request, 'homepage/mypage.html', {
        'recent_comments': recent_comment,
    })

def company(request):
    return render(request, 'homepage/company.html')