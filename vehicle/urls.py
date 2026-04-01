from django.urls import path
from . import views
from .mechanic_views import submit_request_with_mechanic, update_customer_location,customer_request
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # Home and static pages
    path("", views.home, name='home'),
    path('home/', views.home, name='home'), 
    path("contact/", views.contact, name='contact'),
    path("about/", views.about, name='about'),
    
    # Authentication URLs
    path("user_login/", views.user_login, name='user_login'),
    path("user_signup/", views.user_signup, name='user_signup'),
    path("mechanic_login/", views.mechanic_login, name='mechanic_login'),
    path("mechanic_signup/", views.mechanic_signup, name='mechanic_signup'),
    path("admin_login/", views.admin_login, name='admin_login'),
    path("admin_signup/", views.admin_signup, name='admin_signup'),
    path("logout/", views.logout, name='logout'),
    
    # Dashboard URLs
    path("admin_dashboard/", views.admin_dashboard, name='admin_dashboard'),
    path("user_dashboard/", views.user_dashboard, name='user_dashboard'),
    path("mechanic_dashboard/", views.mechanic_dashboard, name='mechanic_dashboard'),
    
    # Admin management URLs
    path("view_personnel/", views.admin_view_all_personnel, name='view_personnel'),
    path("attendance/", views.view_attendance, name='attendance'),
    path("feedback/", views.admin_feedback, name='admin_feedback'),
    path("letter/", views.letter, name='admin_letter'),
    path("contact_admin/", views.view_contact, name='admin_contact'),
    
    # Mechanic URLs
    path("attendance_mechanic/", views.mechanic_attendance, name='mechanic_attendance'),
    
    # Customer URLs
    path("customer_feedback/", views.leave_feedback, name='customer_feedback'),
    path("customer_request/", customer_request, name='customer_request'),
    
    # Traditional CRUD URLs (with page reload)
    path("delete_request/<int:id>/", views.delete_request, name='delete_request'),
    path("update_request/<int:id>/", views.UpdateRequest.as_view(), name='update_request'),
    path("single_customer/<int:id>/", views.get_single_customer, name='single_customer'),
    path("delete_customer/<int:id>/", views.delete_customer, name='delete_customer'),
    path("single_mechanic/<int:id>/", views.get_single_mechanic, name='single_mechanic'),
    path("delete_mechanic/<int:id>/", views.delete_mechanic, name='delete_mechanic'),
    path("admin/update_mechanic/<int:id>/", views.UpdateMechanic.as_view(), name='admin_mechanic_update'),
    path("feedback/<int:id>/", views.delete_feedback, name='delete_feedback'),
    path("attendance/<int:id>/", views.delete_attendance, name='delete_attendance'),
    
    # Map and location URLs
    path('submit-request-with-mechanic/', submit_request_with_mechanic, name='submit_request_with_mechanic'),
    path('update-customer-location/', update_customer_location, name='update_customer_location'),
    
    # ========== API URLs for AJAX CRUD Operations ==========
    # Customer API
    path('admin/api/customer/<int:id>/', views.api_customer_detail, name='api_customer_detail'),
    path('admin/api/customer/add/', views.api_customer_add, name='api_customer_add'),
    path('admin/api/customer/<int:id>/update/', views.api_customer_update, name='api_customer_update'),
    path('admin/api/customer/<int:id>/delete/', views.api_customer_delete, name='api_customer_delete'),
    
    # Mechanic API
    path('admin/api/mechanic/<int:id>/', views.api_mechanic_detail, name='api_mechanic_detail'),
    path('admin/api/mechanic/add/', views.api_mechanic_add, name='api_mechanic_add'),
    path('admin/api/mechanic/<int:id>/update/', views.api_mechanic_update, name='api_mechanic_update'),
    path('admin/api/mechanic/<int:id>/delete/', views.api_mechanic_delete, name='api_mechanic_delete'),
    
    # Request API
    path('admin/api/request/<int:id>/', views.api_request_detail, name='api_request_detail'),
    path('admin/api/request/<int:id>/update/', views.api_request_update, name='api_request_update'),
    path('admin/api/request/<int:id>/delete/', views.api_request_delete, name='api_request_delete'),
    
    # Feedback API
    path('admin/api/feedback/<int:id>/delete/', views.api_feedback_delete, name='api_feedback_delete'),
    
    # Contact API
    path('admin/api/contact/<int:id>/delete/', views.api_contact_delete, name='api_contact_delete'),
    
    # Attendance API
    path('admin/api/attendance/<int:id>/', views.api_attendance_detail, name='api_attendance_detail'),
    path('admin/api/attendance/add/', views.api_attendance_add, name='api_attendance_add'),
    path('admin/api/attendance/<int:id>/update/', views.api_attendance_update, name='api_attendance_update'),
    path('admin/api/attendance/<int:id>/delete/', views.api_attendance_delete, name='api_attendance_delete'),
    
    # Newsletter API
    path('admin/api/newsletter/add/', views.api_newsletter_add, name='api_newsletter_add'),
    path('admin/api/newsletter/<int:id>/delete/', views.api_newsletter_delete, name='api_newsletter_delete'),
    
    
    path('debug-session/', views.debug_session, name='debug_session'),
]

# urlpatterns = [
#     path("", views.home, name='home'),
#     path('home/', views.home, name='home'), 
#     path("user_login/", views.user_login, name='user_login'),
#     path("user_signup/", views.user_signup, name='user_signup'),
#     path("mechanic_login/", views.mechanic_login, name='mechanic_login'),
#     path("mechanic_signup/", views.mechanic_signup, name='mechanic_signup'),
#     path("admin_login/", views.admin_login, name='admin_login'),
#     path("admin_signup/", views.admin_signup, name='admin_signup'),
#     path("logout/", views.logout, name='logout'),
#     path("contact/", views.contact, name='contact'),
#     path("about/", views.about, name='about'),
#     path("admin_dashboard/", views.admin_dashboard, name='admin_dashboard'),
#     path("view_personnel/", views.admin_view_all_personnel, name='view_personnel'),
#     path("user_dashboard/", views.user_dashboard, name='user_dashboard'),
#     path("mechanic_dashboard/", views.mechanic_dashboard, name='mechanic_dashboard'),
#     path("attendance_mechanic/", views.mechanic_attendance, name='mechanic_attendance'),
#     path("customer_feedback/", views.leave_feedback, name='customer_feedback'),
#     path("delete_request/<int:id>/", views.delete_request, name='delete_request'),
#     path("update_request/<int:id>/", views.UpdateRequest.as_view(), name='update_request'),
#     path("single_customer/<int:id>/", views.get_single_customer, name='single_customer'),
#     path("delete_customer/<int:id>/", views.delete_customer, name='delete_customer'),
#     path("single_mechanic/<int:id>/", views.get_single_mechanic, name='single_mechanic'),
#     path("delete_mechanic/<int:id>/", views.delete_mechanic, name='delete_mechanic'),
#     path("admin/update_mechanic/<int:id>/", views.UpdateMechanic.as_view(), name='admin_mechanic_update'),
#     path("feedback/", views.admin_feedback, name='admin_feedback'),
#     path("feedback/<int:id>/", views.delete_feedback, name='delete_feedback'),
#     path("attendance/", views.view_attendance, name='attendance'),
#     path("attendance/<int:id>/", views.delete_attendance, name='delete_attendance'),
#     path("letter/", views.letter, name='admin_letter'),
#     path("contact_admin/", views.view_contact, name='admin_contact'),
    
    
#     path('submit-request-with-mechanic/', submit_request_with_mechanic, name='submit_request_with_mechanic'),
#     path('update-customer-location/', update_customer_location, name='update_customer_location'),
#     path("customer_request/", customer_request, name='customer_request'),
    
    

# ]



