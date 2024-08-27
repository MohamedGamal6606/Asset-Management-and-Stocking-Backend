# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Asset, Inventory

# @receiver(post_save, sender=Asset)
# def create_or_update_inventory(sender, instance, created, **kwargs):
#     # Get the asset name
#     asset_name = instance.name

#     if created:
#         inventory_entries = Inventory.objects.filter(asset__name=asset_name)
        
#         if inventory_entries.exists():
#             # Update the quantity for the related Inventory entry
#             for inventory_entry in inventory_entries:
#                 # Increment quantity or set to a new value if needed
#                 inventory_entry.quantity += 1  # Adjust this as needed
#                 inventory_entry.save()
#         else:
#             # If no Inventory entry exists, create one
#             Inventory.objects.create(asset=instance, quantity=1)
    
