from rest_framework import serializers
from django.contrib.auth import get_user_model
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

    def validate(self, data):
        if 'email' not in data or not data['email']:
            raise serializers.ValidationError("Email is required.")
        if 'username' not in data or not data['username']:
            raise serializers.ValidationError("Username is required.")
        if 'password' not in data or not data['password']:
            raise serializers.ValidationError("Password is required.")
        return data


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'color']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['name', 'completed']


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
            instance.subtasks.all().delete()
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=instance, **subtask_data)

        return instance
