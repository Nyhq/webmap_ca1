import json

from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import LineString
from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404

from .forms import ReviewForm, TrailCreationForm
from .models import Trail, Review
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import csv


def trail_list(request):
    query = request.GET.get('query', '')
    difficulty = request.GET.get('difficulty', '')

    trails = Trail.objects.all()

    if query:
        trails = trails.filter(name__icontains=query)
    if difficulty:
        trails = trails.filter(difficulty=difficulty)

    trails_geojson = serialize('geojson', trails, fields=('name', 'path', 'pk'))
    if request.method == 'POST' and request.user.is_superuser:
        form = TrailCreationForm(request.POST, request.FILES)
        if form.is_valid():
            trail = form.save(commit=False)
            csv_file = form.cleaned_data['csv_file']

            if csv_file:
                # Read and process CSV file to create LineString
                coords = []
                for row in csv.reader(csv_file.read().decode('utf-8').splitlines()):
                    longitude, latitude = row  # Adjust depending on CSV format
                    coords.append((float(longitude), float(latitude)))
                trail.path = LineString(coords)

            trail.save()
            return redirect('trail_list')
    else:
        form = TrailCreationForm()

    return render(request, 'trail_list.html', {
        'trails': trails,
        'trails_geojson': trails_geojson
    })


def trail_detail(request, pk):
    trail = get_object_or_404(Trail, pk=pk)
    reviews = Review.objects.filter(trail=trail)

    # Serialize the trail's path to GeoJSON
    trail_geojson = serialize('geojson', [trail], fields=('name', 'path'))
    # Convert to Python dict and then back to JSON string to ensure proper formatting
    trail_geojson = json.loads(trail_geojson)
    trail_geojson = json.dumps(trail_geojson['features'][0])  # Extract the single feature

    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.trail = trail
            new_review.author = request.user
            new_review.save()

            # Redirect to the same page to prevent duplicate submissions
            return redirect('trail_detail', pk=trail.pk)
    else:
        review_form = ReviewForm()

    return render(request, 'trail_detail.html', {
        'trail': trail,
        'trail_geojson': trail_geojson,
        'reviews': reviews,
        'review_form': review_form
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page after registration
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
