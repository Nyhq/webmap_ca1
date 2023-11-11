import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404

from .forms import ReviewForm
from .models import Trail, Review
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def trail_list(request):
    trails = Trail.objects.all()
    trails_geojson = serialize('geojson', trails, fields=('name', 'path'))

    return render(request, 'trail_list.html', {
        'trails': trails,
        'trails_geojson': trails_geojson
    })


@login_required
def trail_detail(request, pk):
    trail = get_object_or_404(Trail, pk=pk)
    reviews = Review.objects.filter(trail=trail)
    new_review = None

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
    else:
        review_form = ReviewForm()

    return render(request, 'trail_detail.html', {
        'trail': trail,
        'trail_geojson': trail_geojson,
        'reviews': reviews,
        'new_review': new_review,
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