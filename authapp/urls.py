from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, UpdateTaskStatusView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
]


