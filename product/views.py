from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Category, Company, Tag, Comment
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.product   # method = post 방식
    if request.user.is_authenticated and request.user == comment.author :
      comment.delete()
      return  redirect(post.get_absolute_url())   # method = post 방식
    else:
        PermissionDenied

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'price', 'color', 'info', 'image', 'category', 'company', 'tags']
    template_name = 'product/product_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):  ##추가인자##
        context = super(ProductUpdate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count
        context['companies'] = Company.objects.all()
        context['no_company_product_count'] = Product.objects.filter(category=None).count
        return context


class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'color', 'info', 'image', 'category', 'company', 'tags']
    #모델명_form.html

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff     # or 둘 중 하나만 만족

    def form_valid(self, form):      #로그인 해야 PostCreate 사용 가능, 작성자 자동 입력
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):      # and 둘 다 만족
            form.instance.author = current_user
            return super(ProductCreate, self).form_valid(form)
        else:
            return redirect('/product/')

    def get_context_data(self, *, object_list=None, **kwargs):  ##추가인자##
        context = super(ProductCreate,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Product.objects.filter(category=None).count
        context['companies'] = Company.objects.all()
        context['no_company_product_count'] = Product.objects.filter(category=None).count
        return context


class ProductList(ListView):
    model = Product
    ordering = '-pk'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):  ##추가인자##
        context = super(ProductList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count
        context['companies'] = Company.objects.all()
        context['no_company_product_count'] = Product.objects.filter(category=None).count
        return context


class ProductSearch(ProductList): #ListView 상속
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        product_list = Product.objects.filter(Q(name__contains=q) | Q(tags__name__contains=q)).distinct()
        return product_list

    def get_context_data(self, **kwargs):
        context = super(ProductSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context


class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):  ##추가인자##
        context = super(ProductDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count
        context['companies'] = Company.objects.all()
        context['no_company_product_count'] = Product.objects.filter(category=None).count
        context['comment_form'] = CommentForm
        return context

def new_comment(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:  # GET
            return redirect(product.get_absolute_url())
    else:  # 로그인 안 한 사용자
         raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    # 템플릿: comment_form

    def dispatch(self, request, *args, **kwargs):
         if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
         else:
            raise PermissionDenied


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        product_list = Product.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        product_list = Product.objects.filter(category=category)
    return render(request, 'product/product_list.html', {
        'category' : category,
        'product_list' : product_list,
        'categories' : Category.objects.all(),
        'no_category_product_count' : Product.objects.filter(category=None).count
    })

def company_page(request, slug):
    if slug == 'no_company':
        company = '미분류'
        product_list = Product.objects.filter(company=None)
    else :
        company = Company.objects.get(slug=slug)
        product_list = Product.objects.filter(company=company)
    return render(request, 'product/product_list.html', {
        'company' : company,
        'product_list' : product_list,
        'companies' : Company.objects.all(),
        'no_company_product_count' : Product.objects.filter(company=None).count
    })

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    product_list = tag.product_set.all()
    return render(request, 'product/product_list.html', {
            'tag' : tag,
            'product_list' : product_list,
            'categories': Category.objects.all(),
            'no_category_product_count': Product.objects.filter(category=None).count
            })