from graphene_django import DjangoObjectType
import graphene
from createTodo.models import Category, Todo
from graphene_django.rest_framework.mutation import SerializerMutation
from createTodo.serializers import CategorySerializer, TodoSerializer


class CategoryObjectType(DjangoObjectType):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "parent",
            "slug",
            "is_active",
        )


class TodoObjectType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = (
            "id",
            "owner",
            "category",
            "todo_title",
            "todo_description",
            "created_at",
            "updated_at",
            "status",
        )


class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryObjectType)
    category = graphene.Field(CategoryObjectType, slug=graphene.String())
    all_todos_by_category = graphene.List(TodoObjectType, slug=graphene.String())

    all_todos = graphene.List(TodoObjectType)
    todo = graphene.Field(TodoObjectType, slug=graphene.String())

    def resolve_all_categories(root, info):
        return Category.objects.all().order_by("-id")

    def resolve_all_todos_by_category(root, info, slug):
        return Todo.objects.filter(category__slug__iexact=slug)

    def resolve_category(root, info, slug):
        try:
            if info.context.user.is_active:
                category = Category.objects.get(slug=slug)
                if (
                        info.context.user.is_active and
                        info.context.user == category.owner
                ):
                    return category
                else:
                    return {
                        "404NotFound": "Object not found"
                    }

        except Category.DoesNotExist:
            return {
                "404NotFound": "Object not found"
            }

    def resolve_all_todos(root, info):
        return Todo.objects.all().order_by("-id")

    def resolve_todo(root, info, slug):
        try:
            if info.context.user.is_active:
                todo = Todo.objects.get(slug=slug)
                if (
                        info.context.user.is_active and
                        info.context.user == todo.owner
                ):
                    return todo
                else:
                    return {
                        "404NotFound": "Object not found"
                    }

        except Todo.DoesNotExist:
            return {
                "404NotFound": "Object not found"
            }


class CategoryMutation(SerializerMutation):
    class Meta:
        serializer_class = CategorySerializer
        model_operations = ("create", "update")
        lookup_field = "slug"


class TodoMutation(SerializerMutation):
    class Meta:
        serializer_class = TodoSerializer
        model_operations = ("create", "update")
        lookup_field = "slug"


class DeleteCategoryMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **input):
        category = Category.objects.get(pk=input["id"])
        category.delete()
        return cls(ok=True)


class DeleteTodoMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **input):
        todo = Todo.objects.get(pk=input["id"])
        todo.delete()
        return cls(ok=True)


class Mutation(graphene.ObjectType):
    create_and_update_category = CategoryMutation.Field()
    create_and_update_todo = TodoMutation.Field()

    delete_category = DeleteCategoryMutation.Field()
    delete_todo = DeleteTodoMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
