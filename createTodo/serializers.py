from rest_framework import serializers
from createTodo.models import Category, Todo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "owner",
            "name",
            "slug",
            "parent",
            "is_active",
        )


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            "id",
            "owner",
            "todo_title",
            "todo_description",
            "slug",
            "created_at",
            "updated_at",
            "status",
            "category",
        )
