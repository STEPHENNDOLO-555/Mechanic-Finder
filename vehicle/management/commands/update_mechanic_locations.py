# management/commands/update_mechanic_locations.py
from django.core.management.base import BaseCommand
from vehicle.models import Mechanic

class Command(BaseCommand):
    help = 'Update mechanic locations with realistic coordinates and set hired=True'

    def handle(self, *args, **options):
        # First, list all mechanics before update
        self.stdout.write("Current mechanics in database BEFORE update:")
        all_mechanics = Mechanic.objects.all()
        self.stdout.write(f"Total mechanics: {all_mechanics.count()}")
        
        for m in all_mechanics:
            self.stdout.write(f"  ID: {m.id}, Name: {m.username}, Hired: {m.hired}, Lat: {m.latitude}, Lon: {m.longitude}")
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write("Updating mechanics...\n")
        
        # Coordinates for mechanics with IDs 3-9
        mechanic_updates = {
    3: {
        'latitude': -1.3845056,      # Same as customer (0km)
        'longitude': 36.8377856,
        'direction': 'Center',
        'distance': 0
    },
    4: {
        'latitude': -0.5000000,      # 100km North
        'longitude': 36.8377856,
        'direction': 'North',
        'distance': 100
    },
    5: {
        'latitude': -2.0690000,      # 100km South
        'longitude': 36.8377856,
        'direction': 'South',
        'distance': 100
    },
    6: {
        'latitude': -1.2845056,      # 100km East
        'longitude': 37.8377856,
        'direction': 'East',
        'distance': 100
    },
    7: {
        'latitude': -1.2845056,      # 100km West
        'longitude': 35.8377856,
        'direction': 'West',
        'distance': 100
    },
    8: {
        'latitude': -0.5000000,      # 100km Northeast
        'longitude': 37.3377856,
        'direction': 'Northeast',
        'distance': 100
    },
    9: {
        'latitude': -2.0690000,      # 100km Southeast
        'longitude': 37.3377856,
        'direction': 'Southeast',
        'distance': 100
    },
}
        
        updated = 0
        for mechanic_id, coords in mechanic_updates.items():
            try:
                mechanic = Mechanic.objects.get(id=mechanic_id)
                
                # Store old values
                old_hired = mechanic.hired
                old_lat = mechanic.latitude
                old_lon = mechanic.longitude
                
                # Update coordinates AND set hired=True
                mechanic.latitude = coords['latitude']
                mechanic.longitude = coords['longitude']
                mechanic.hired = True  # Set hired to True
                mechanic.save()
                
                updated += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Updated ID {mechanic_id}: {mechanic.username}\n"
                        f"   Hired: {old_hired} → True\n"
                        f"   Location: ({old_lat}, {old_lon}) → ({mechanic.latitude}, {mechanic.longitude})"
                    )
                )
            except Mechanic.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"❌ Mechanic with ID {mechanic_id} does not exist")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error updating ID {mechanic_id}: {e}")
                )
        
        # Update any other mechanics that don't have coordinates or are not hired
        self.stdout.write("\n" + "="*50)
        self.stdout.write("Updating other mechanics to hired=True if they have coordinates...")
        
        # Set all mechanics with valid coordinates to hired=True
        other_updated = Mechanic.objects.filter(
            latitude__isnull=False, 
            longitude__isnull=False
        ).exclude(id__in=mechanic_updates.keys()).update(hired=True)
        
        if other_updated > 0:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Updated {other_updated} other mechanics to hired=True")
            )
        
        # Verify all updates
        self.stdout.write("\n" + "="*50)
        self.stdout.write("Verification AFTER update:")
        verified_mechanics = Mechanic.objects.filter(id__in=[3,4,5,6,7,8,9])
        
        for m in verified_mechanics:
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✅ ID: {m.id}, Name: {m.username}, Hired: {m.hired}, "
                    f"Lat: {m.latitude}, Lon: {m.longitude}"
                )
            )
        
        # Show summary of all mechanics
        self.stdout.write("\n" + "="*50)
        self.stdout.write("Final Summary of ALL mechanics:")
        all_mechanics_final = Mechanic.objects.all()
        for m in all_mechanics_final:
            status = "✅" if m.hired and m.latitude and m.longitude else "⚠️"
            self.stdout.write(
                f"  {status} ID: {m.id}, Name: {m.username}, Hired: {m.hired}, "
                f"Lat: {m.latitude}, Lon: {m.longitude}"
            )
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully updated {updated} mechanics with coordinates and set hired=True"))
        if other_updated > 0:
            self.stdout.write(self.style.SUCCESS(f"✅ Also set hired=True for {other_updated} other mechanics with coordinates"))