from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view()),                 # product_list
    path('<int:pk>/', views.ProductDetail.as_view()),      # product_detail

    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),

    path('category/<str:slug>/', views.category_page),   # IP주소/blog/category/slug/
    path('company/<str:slug>/', views.company_page),

    path('create_product/', views.ProductCreate.as_view()),
    path('update_product/<int:pk>/', views.ProductUpdate.as_view()),

    path('tag/<str:slug>/', views.tag_page),

    path('search/<str:q>/', views.ProductSearch.as_view()),

]