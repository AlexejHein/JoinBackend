from rest_framework import serializers
from django.contrib.auth import get_user_model
from authapp.models import Contact, Task, Subtask

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
        fields = ['id', 'name', 'email', 'phone', ]
        # read_only_fields = ['user']


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['name', 'completed']


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), source='assigned_to.id')

    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'assigned_to', 'due_date', 'priority', 'subtasks']

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        task = Task.objects.create(**validated_data)
        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)
        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()

        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id')
            if subtask_id:
                subtask = Subtask.objects.get(id=subtask_id, task=instance)
                subtask.name = subtask_data.get('name', subtask.name)
                subtask.completed = subtask_data.get('completed', subtask.completed)
                subtask.save()
            else:
                Subtask.objects.create(task=instance, **subtask_data)

        return instance
