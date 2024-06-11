from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from authapp.models import Contact, Task, Subtask, Category

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'color']


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['name', 'completed']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True)
    assigned_to = serializers.SlugRelatedField(slug_field='name', queryset=Contact.objects.all())
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    category = serializers.CharField()
    categoryColor = serializers.CharField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'categoryColor', 'assigned_to', 'due_date', 'priority',
                  'status', 'subtasks']
        extra_kwargs = {
            'due_date': {'required': True},
        }

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        category_name = validated_data.pop('category')
        category_color = validated_data.pop('categoryColor', None)

        # Hier speichern wir den Farbwert direkt
        validated_data['category'] = category_name
        validated_data['categoryColor'] = category_color if category_color else '#ffffff'

        task = Task.objects.create(**validated_data)

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', None)
        category_name = validated_data.pop('category', None)
        category_color = validated_data.pop('categoryColor', None)

        if category_name:
            instance.category = category_name
        if category_color:
            instance.categoryColor = category_color

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if subtasks_data is not None:
            for subtask_data in subtasks_data:
                subtask_id = subtask_data.get('id')
                if subtask_id:
                    try:
                        subtask = Subtask.objects.get(id=subtask_id, task=instance)
                    except Subtask.DoesNotExist:
                        subtask = Subtask.objects.create(task=instance, **subtask_data)
                    subtask.name = subtask_data.get('name', subtask.name)
                    subtask.completed = subtask_data.get('completed', subtask.completed)
                    subtask.save()
                else:
                    Subtask.objects.create(task=instance, **subtask_data)

        return instance

