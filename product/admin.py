from django.contrib import admin
from .models import Product, Company, Category, Tag, Comment

admin.site.register(Product)

class CompanyAdmin(admin.ModelAdmin):    ## slug ##
    prepopulated_fields = {'slug' : ('name', )}
admin.site.register(Company, CompanyAdmin)

class CategoryAdmin(admin.ModelAdmin):    ## slug ##
    prepopulated_fields = {'slug' : ('name', )}
admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
admin.site.register(Tag, TagAdmin)

admin.site.register(Comment)
