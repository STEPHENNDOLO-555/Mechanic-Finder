from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import math
import json
from vehicle.models import Customer, Mechanic, Request

def customer_request(request):
    """Main customer request view - shows map with mechanics and modal form"""
    # Check if user is logged in
    if not request.session.get('username', None):
        return redirect('login')
    
    # Redirect based on user type
    if request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    
    # Only customers can access this view
    if request.session.get('type', None) != 'customer':
        return redirect('home')
    
    username = request.session['username']
    customer = Customer.objects.get(username=username)
    
    # Calculate distance function (Haversine formula)
    def calculate_distance(lat1, lon1, lat2, lon2):
        if not all([lat1, lon1, lat2, lon2]):
            return float('inf')
        
        R = 6371  # Earth's radius in kilometers
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    # Get all mechanics with location data
    mechanics = Mechanic.objects.filter(hired=True, latitude__isnull=False, longitude__isnull=False)
    
    # Calculate distance for each mechanic if customer has location
    mechanics_data = []
    customer_has_location = customer.latitude and customer.longitude
    
    if customer_has_location:
        for mechanic in mechanics:
            distance = calculate_distance(
                customer.latitude, customer.longitude,
                mechanic.latitude, mechanic.longitude
            )
            if distance <= 1000:  # Within 1000 kilometers
                mechanics_data.append({
                    'id': mechanic.id,
                    'username': mechanic.username,
                    'latitude': float(mechanic.latitude),
                    'longitude': float(mechanic.longitude),
                    'skill': mechanic.skill,
                    'phone': mechanic.phone,
                    'location': mechanic.location,
                    'distance': round(distance, 2),
                    'image_url': mechanic.get_image_url
                })
        # Sort by distance
        mechanics_data.sort(key=lambda x: x['distance'])
    else:
        # If customer doesn't have location, show all mechanics without distance
        for mechanic in mechanics:
            mechanics_data.append({
                'id': mechanic.id,
                'username': mechanic.username,
                'latitude': float(mechanic.latitude),
                'longitude': float(mechanic.longitude),
                'skill': mechanic.skill,
                'phone': mechanic.phone,
                'location': mechanic.location,
                'distance': None,
                'image_url': mechanic.get_image_url
            })
    
    context = {
        'mechanics': mechanics_data,
        'customer': customer,
        'customer_has_location': customer_has_location,
        'mechanics_json': json.dumps(mechanics_data)  # Pass JSON for JavaScript
    }
    
    return render(request, 'customers/request_form.html', context)

@csrf_exempt
def submit_request_with_mechanic(request):
    """Handle AJAX request submission with mechanic selection"""
    if request.method == 'POST' and request.session.get('type') == 'customer':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            mechanic_id = data.get('mechanic_id')
            category = data.get('category')
            vehicle_no = data.get('vehicle_no')
            vehicle_name = data.get('vehicle_name')
            vehicle_brand = data.get('vehicle_brand')
            vehicle_model = data.get('vehicle_model')
            problem_description = data.get('problem_description')
            
            # Validate required fields
            if not all([mechanic_id, category, vehicle_no, vehicle_name, vehicle_brand, vehicle_model, problem_description]):
                return JsonResponse({'success': False, 'error': 'Please fill in all fields'})
            
            # Get customer and mechanic
            username = request.session['username']
            customer = Customer.objects.get(username=username)
            mechanic = Mechanic.objects.get(id=mechanic_id, hired=True)
            
            # Create request
            problem = Request(
                customer=customer,
                mechanic=mechanic,
                category=category,
                vehicle_no=vehicle_no,
                vehicle_name=vehicle_name,
                vehicle_brand=vehicle_brand,
                vehicle_model=vehicle_model,
                problem_description=problem_description,
                status='Pending'
            )
            problem.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Request sent successfully to {mechanic.username}'
            })
            
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Customer not found'})
        except Mechanic.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mechanic not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def update_customer_location(request):
    """Update customer location from browser geolocation"""
    if request.method == 'POST' and request.session.get('type') == 'customer':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            username = request.session['username']
            customer = Customer.objects.get(username=username)
            customer.latitude = latitude
            customer.longitude = longitude
            customer.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})