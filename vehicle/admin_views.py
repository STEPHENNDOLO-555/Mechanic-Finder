from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import json
from vehicle.models import Customer, Mechanic, Request, Feedback, Attendance, Contact, News, Admin
from functools import wraps

# Helper function to check admin session
def is_admin_logged_in(request):
    """Check if user is logged in as admin"""
    return request.session.get('username') and request.session.get('type') == 'admin'

def admin_required(view_func):
    """Decorator to ensure user is logged in as admin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_admin_logged_in(request):
            return JsonResponse({'success': False, 'error': 'Unauthorized - Please login as admin'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_dashboard(request):
    """Admin dashboard view with session authentication"""
    # Check if user is logged in and is admin
    if request.session.get('username') and request.session.get('type') == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username') and request.session.get('type') == 'customer':
        return redirect('user_dashboard')
    if request.session.get('username') and request.session.get('type') == 'admin':
        try:
            username = request.session['username']
            name = Admin.objects.get(username=username)
            
            context = {
                'admin': name,
                'customer_count': Customer.objects.count(),
                'mechanic_count': Mechanic.objects.filter(hired=True).count(),
                'request_count': Request.objects.count(),
                'feedback_count': Feedback.objects.count(),
                'customers': Customer.objects.all().order_by('-id')[:20],
                'mechanics': Mechanic.objects.all().order_by('-id')[:20],
                'all_requests': Request.objects.select_related('customer', 'mechanic').all().order_by('-date'),
                'recent_requests': Request.objects.select_related('customer').all().order_by('-date')[:10],
                'feedbacks': Feedback.objects.all().order_by('-date')[:20],
                'attendances': Attendance.objects.select_related('mechanic').all().order_by('-date')[:20],
                'contacts': Contact.objects.all().order_by('-id')[:20],
                'newsletters': News.objects.all().order_by('-id')[:20],
            }
            return render(request, 'admin/admin_dashboard.html', context)
        except Admin.DoesNotExist:
            # Clear invalid session
            request.session.flush()
            return redirect('admin_login')
    else:
        return redirect('admin_login')

# ========== API Views with Proper Authentication ==========

@admin_required
def api_customer_detail(request, id):
    """Get customer details"""
    try:
        customer = get_object_or_404(Customer, id=id)
        return JsonResponse({
            'id': customer.id,
            'username': customer.username,
            'email': customer.email,
            'phone': customer.phone,
            'location': customer.location,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@admin_required
def api_customer_add(request):
    """Add new customer"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            password_hash = make_password(data['password'])
            customer = Customer.objects.create(
                username=data['username'],
                email=data['email'],
                phone=data['phone'],
                location=data['location'],
                password=password_hash
            )
            return JsonResponse({'success': True, 'message': 'Customer added successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@admin_required
def api_customer_update(request, id):
    """Update customer"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer = get_object_or_404(Customer, id=id)
            customer.username = data.get('username', customer.username)
            customer.email = data.get('email', customer.email)
            customer.phone = data.get('phone', customer.phone)
            customer.location = data.get('location', customer.location)
            if data.get('password'):
                customer.password = make_password(data['password'])
            customer.save()
            return JsonResponse({'success': True, 'message': 'Customer updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@admin_required
def api_customer_delete(request, id):
    """Delete customer"""
    if request.method == 'POST':
        try:
            customer = get_object_or_404(Customer, id=id)
            customer.delete()
            return JsonResponse({'success': True, 'message': 'Customer deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Mechanic API Views
@admin_required
def api_mechanic_detail(request, id):
    """Get mechanic details"""
    try:
        mechanic = get_object_or_404(Mechanic, id=id)
        return JsonResponse({
            'id': mechanic.id,
            'username': mechanic.username,
            'email': mechanic.email,
            'phone': mechanic.phone,
            'location': mechanic.location,
            'skill': mechanic.skill,
            'salary': mechanic.salary,
            'hired': mechanic.hired,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@admin_required
def api_mechanic_add(request):
    """Add new mechanic"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            password_hash = make_password(data['password'])
            mechanic = Mechanic.objects.create(
                username=data['username'],
                email=data['email'],
                phone=data['phone'],
                location=data['location'],
                skill=data['skill'],
                salary=data.get('salary'),
                hired=data.get('hired', False),
                password=password_hash
            )
            return JsonResponse({'success': True, 'message': 'Mechanic added successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@admin_required
def api_mechanic_update(request, id):
    """Update mechanic"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mechanic = get_object_or_404(Mechanic, id=id)
            mechanic.username = data.get('username', mechanic.username)
            mechanic.email = data.get('email', mechanic.email)
            mechanic.phone = data.get('phone', mechanic.phone)
            mechanic.location = data.get('location', mechanic.location)
            mechanic.skill = data.get('skill', mechanic.skill)
            mechanic.salary = data.get('salary', mechanic.salary)
            mechanic.hired = data.get('hired', mechanic.hired)
            if data.get('password'):
                mechanic.password = make_password(data['password'])
            mechanic.save()
            return JsonResponse({'success': True, 'message': 'Mechanic updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@admin_required
def api_mechanic_delete(request, id):
    """Delete mechanic"""
    if request.method == 'POST':
        try:
            mechanic = get_object_or_404(Mechanic, id=id)
            mechanic.delete()
            return JsonResponse({'success': True, 'message': 'Mechanic deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Request API Views
@admin_required
def api_request_detail(request, id):
    """Get request details"""
    try:
        req = get_object_or_404(Request, id=id)
        return JsonResponse({
            'id': req.id,
            'status': req.status,
            'cost': req.cost,
            'mechanic_id': req.mechanic.id if req.mechanic else None,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@admin_required
def api_request_update(request, id):
    """Update request"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            req = get_object_or_404(Request, id=id)
            req.status = data.get('status', req.status)
            req.cost = data.get('cost', req.cost)
            if data.get('mechanic_id'):
                req.mechanic_id = data['mechanic_id']
            req.save()
            return JsonResponse({'success': True, 'message': 'Request updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@admin_required
def api_request_delete(request, id):
    """Delete request"""
    if request.method == 'POST':
        try:
            req = get_object_or_404(Request, id=id)
            req.delete()
            return JsonResponse({'success': True, 'message': 'Request deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Feedback API
@admin_required
def api_feedback_delete(request, id):
    """Delete feedback"""
    if request.method == 'POST':
        try:
            feedback = get_object_or_404(Feedback, id=id)
            feedback.delete()
            return JsonResponse({'success': True, 'message': 'Feedback deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Contact API
@admin_required
def api_contact_delete(request, id):
    """Delete contact"""
    if request.method == 'POST':
        try:
            contact = get_object_or_404(Contact, id=id)
            contact.delete()
            return JsonResponse({'success': True, 'message': 'Contact deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Attendance API
@admin_required
def api_attendance_detail(request, id):
    """Get attendance details"""
    try:
        attendance = get_object_or_404(Attendance, id=id)
        return JsonResponse({
            'id': attendance.id,
            'mechanic_id': attendance.mechanic.id,
            'present_status': attendance.present_status,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@admin_required
def api_attendance_add(request):
    """Add attendance"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance = Attendance.objects.create(
                mechanic_id=data['mechanic_id'],
                present_status=data['present_status']
            )
            return JsonResponse({'success': True, 'message': 'Attendance marked successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@admin_required
def api_attendance_update(request, id):
    """Update attendance"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance = get_object_or_404(Attendance, id=id)
            attendance.mechanic_id = data.get('mechanic_id', attendance.mechanic_id)
            attendance.present_status = data.get('present_status', attendance.present_status)
            attendance.save()
            return JsonResponse({'success': True, 'message': 'Attendance updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@admin_required
def api_attendance_delete(request, id):
    """Delete attendance"""
    if request.method == 'POST':
        try:
            attendance = get_object_or_404(Attendance, id=id)
            attendance.delete()
            return JsonResponse({'success': True, 'message': 'Attendance deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Newsletter API
@admin_required
def api_newsletter_add(request):
    """Add newsletter subscriber"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            newsletter = News.objects.create(email=data['email'])
            return JsonResponse({'success': True, 'message': 'Subscriber added successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@admin_required
def api_newsletter_delete(request, id):
    """Delete newsletter subscriber"""
    if request.method == 'POST':
        try:
            newsletter = get_object_or_404(News, id=id)
            newsletter.delete()
            return JsonResponse({'success': True, 'message': 'Subscriber deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)