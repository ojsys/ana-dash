from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from .models import Farmer, Partner, Event, ExtensionAgent, Dissemination
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
import csv
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import  AuthenticationForm
from .forms import SimpleSignupForm



def signup_view(request):
    if request.method == 'POST':
        form = SimpleSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to your main dashboard view
    else:
        form = SimpleSignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to your main dashboard view
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})




@login_required
def dashboard(request):
    # Basic statistics
    total_farmers = Farmer.objects.count()
    total_events = Event.objects.count()
    total_extension_agents = ExtensionAgent.objects.count()
    active_partners = Partner.objects.count()
    

    # Gender distribution
    gender_distribution = Farmer.objects.values('gender').annotate(count=Count('gender'))

    # Top 10 cities by farmer count
    top_cities = Farmer.objects.values('partner__country').annotate(count=Count('id')).order_by('-count')[:10]

    # Top 10 partners by farmer count
    top_partners = Partner.objects.annotate(farmer_count=Count('farmer')).order_by('-farmer_count')[:10]

    # Events over time
    events_over_time = Event.objects.annotate(month=TruncMonth('startdate')).values('month').annotate(count=Count('id')).order_by('month')

    # Crop distribution
    crop_distribution = {
        'Cassava': Farmer.objects.filter(cassava=True).count(),
        'Yam': Farmer.objects.filter(yam=True).count(),
        'Maize': Farmer.objects.filter(maize=True).count(),
        'Rice': Farmer.objects.filter(rice=True).count(),
        'Sorghum': Farmer.objects.filter(sorghum=True).count(),
    }

    # Recent events
    recent_events = Event.objects.filter(startdate__gte=timezone.now() - timezone.timedelta(days=30)).order_by('-startdate')[:5]

    # Farmers reached through dissemination
    farmers_reached = Dissemination.objects.aggregate(
        male=Sum('farmers_M'),
        female=Sum('farmers_F')
    )

    context = {
        'total_farmers': total_farmers,
        'total_events': total_events,
        'total_extension_agents': total_extension_agents,
        'active_partners': active_partners,
        'gender_distribution': list(gender_distribution),
        'top_cities': list(top_cities),
        'top_partners': list(top_partners),
        'events_over_time': list(events_over_time),
        'crop_distribution': crop_distribution,
        'recent_events': recent_events,
        'farmers_reached': farmers_reached,
    }

    return render(request, 'dashboard/dashboard.html', context)


def dashboard_update(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter querysets based on the date range
    farmers = Farmer.objects.filter(registration_date__range=[start_date, end_date])
    events = Event.objects.filter(startdate__range=[start_date, end_date])
    extension_agents = ExtensionAgent.objects.filter(registration_date__range=[start_date, end_date])
    partners = Partner.objects.filter(registration_date__range=[start_date, end_date])

    # Recalculate metrics based on filtered querysets
    total_farmers = farmers.count()
    total_events = events.count()
    total_extension_agents = extension_agents.count()
    active_partners = partners.count()

    gender_distribution = farmers.values('gender').annotate(count=Count('gender'))
    top_cities = farmers.values('partner__country').annotate(count=Count('id')).order_by('-count')[:10]
    top_partners = partners.annotate(farmer_count=Count('farmer')).order_by('-farmer_count')[:10]
    events_over_time = events.annotate(month=TruncMonth('startdate')).values('month').annotate(count=Count('id')).order_by('month')

    crop_distribution = {
        'Cassava': farmers.filter(cassava=True).count(),
        'Yam': farmers.filter(yam=True).count(),
        'Maize': farmers.filter(maize=True).count(),
        'Rice': farmers.filter(rice=True).count(),
        'Sorghum': farmers.filter(sorghum=True).count(),
    }

    farmers_reached = Dissemination.objects.filter(date__range=[start_date, end_date]).aggregate(
        male=Sum('farmers_M'),
        female=Sum('farmers_F')
    )

    data = {
        'total_farmers': total_farmers,
        'total_events': total_events,
        'total_extension_agents': total_extension_agents,
        'active_partners': active_partners,
        'gender_distribution': list(gender_distribution),
        'top_cities': list(top_cities),
        'top_partners': list(top_partners),
        'events_over_time': list(events_over_time),
        'crop_distribution': crop_distribution,
        'farmers_reached': farmers_reached,
    }

    return JsonResponse(data)


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # An admin-only dashboard with more detailed analytics
    pass



def export_farmers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="farmers.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Gender', 'Crops'])

    farmers = Farmer.objects.all().values_list('firstname', 'lastname', 'gender', 'crops')
    for farmer in farmers:
        writer.writerow(farmer)

    return response


def get_dashboard_data():
    cache_key = 'dashboard_data'
    data = cache.get(cache_key)
    if data is None:
        # Your data fetching logic here
        data = {
            'total_farmers': Farmer.objects.count(),
            # ... other data ...
        }
        cache.set(cache_key, data, 3600)  # Cache for 1 hour
    return data