from django.urls import path
from .views import RegisterUserView, RegisterStaffUserView, RegisterSuperUserView, LoginView, LogoutView, ActivateUserView, DeactivateUserView, StaffUsersView, AgencyView, EditAgencyView

urlpatterns = [
  path('register/', RegisterUserView.as_view(), name='register_user'),
  path('register/staff/', RegisterStaffUserView.as_view(), name='register_staff'),
  path('register/superuser/', RegisterSuperUserView.as_view(), name='register_superuser'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('activate/<int:user_id>/', ActivateUserView.as_view(), name='activate_user'),
  path('deactivate/<int:user_id>/', DeactivateUserView.as_view(), name='deactivate_user'),
  path('non-staff-users/', StaffUsersView.as_view(), name='non-staff-users'),
  path('agency/', AgencyView.as_view(), name='create_agency'),
  path('agency/edit/<int:agency_id>/', EditAgencyView.as_view(), name='edit_agency'),
  path('agency/<int:id>/', AgencyView.as_view(), name='agency-detail'),
]
