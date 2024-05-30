from django.http import JsonResponse
from django.views import View
from rest_framework import generics, viewsets
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact, Task
from .serializers import UserSerializer, ContactSerializer, TaskSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            print("Error saving task:", e)
            raise


class UpdateTaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def update_task_status(self, task, status):
        task.status = status
        task.save()
        return task

    def put(self, request, *args, **kwargs):
        title = request.data.get('title')
        due_date = request.data.get('due_date')
        assigned_to = request.data.get('assigned_to')  # Assuming this is a string
        status = request.data.get('status')

        # Debugging Statements
        print("Title:", title)
        print("Due Date:", due_date)
        print("Assigned To:", assigned_to)
        print("Status:", status)

        try:
            task = get_object_or_404(Task, title=title, due_date=due_date, assigned_to__name=assigned_to)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        updated_task = self.update_task_status(task, status)
        serializer = TaskSerializer(updated_task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestView(View):
    def get(self, request):
        return JsonResponse({"message": "Test view is working!"})
