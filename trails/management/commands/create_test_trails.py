from django.core.management.base import BaseCommand
from django.contrib.gis.geos import LineString
from trails.models import Trail  # Replace with your actual app and model
import random


class Command(BaseCommand):
    help = 'Generates individual test trails with Irish data'

    def create_trail(self, name, description, difficulty, coords):
        line = LineString(coords)
        trail = Trail(name=name, description=description, difficulty=difficulty, path=line)
        trail.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created {trail.name} with length {trail.length} km'))

    def handle(self, *args, **kwargs):
        # Create individual trails
        self.create_trail(
            name="Dublin Trail",
            description="Test trail in Dublin",
            difficulty="Easy",
            coords=[(-6.260310, 53.349805), (-6.2675, 53.3489), (-6.2597, 53.3478), (-6.260310, 53.349805)]
        )
        self.create_trail(
            name="Limerick Trail",
            description="Test trail in Limerick",
            difficulty="Medium",
            coords=[(-8.626734, 52.663837), (-8.6246, 52.6629), (-8.6258, 52.6648), (-8.626734, 52.663837)]
        )
        self.create_trail(
            name="Cork Trail",
            description="Test trail in Cork",
            difficulty="Hard",
            coords=[(-8.486316, 51.896891), (-8.4850, 51.8979), (-8.4873, 51.8958), (-8.486316, 51.896891)]
        )