from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authapp.views import ContactViewSet, TaskViewSet, UpdateTaskStatusView

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authapp.urls')),
    path('api/', include(router.urls)),
    path('api/tasks/updatestatus/', UpdateTaskStatusView.as_view(), name='update_task_status'),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
]
