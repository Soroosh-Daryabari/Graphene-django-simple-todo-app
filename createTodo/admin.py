from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from createTodo.models import Category, Todo


admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Todo)
