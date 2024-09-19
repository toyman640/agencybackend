from django.urls import path
from .views import RegisterUserView, RegisterStaffUserView, RegisterSuperUserView, LoginView, LogoutView, ActivateUserView, DeactivateUserView

urlpatterns = [
  path('register/', RegisterUserView.as_view(), name='register_user'),
  path('register/staff/', RegisterStaffUserView.as_view(), name='register_staff'),
  path('register/superuser/', RegisterSuperUserView.as_view(), name='register_superuser'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('activate/<int:user_id>/', ActivateUserView.as_view(), name='activate_user'),
  path('deactivate/<int:user_id>/', DeactivateUserView.as_view(), name='deactivate_user'),
]
