from io import BytesIO
import uuid
from django.db import models
from django.dispatch import receiver
from django.forms import ValidationError
from django.utils import timezone
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
import os
from django.conf import settings
from django.db.models.signals import post_delete
from solo.models import SingletonModel
class Country(models.Model):
    
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Governate(models.Model):
    
    country= models.ForeignKey(Country, on_delete=models.CASCADE,null=True, blank=False, related_name='governates')
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.country.name})"

class Area(models.Model):
    
    governate= models.ForeignKey(Governate, on_delete=models.CASCADE,null=True, blank=False, related_name='areas')
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f"{self.name} ({self.governate.name}, {self.governate.country.name})"

class Building(models.Model):
    
    area= models.ForeignKey(Area, on_delete=models.CASCADE,null=True, blank=False, related_name='buildings')
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.area.name}, {self.area.governate.name}, {self.area.governate.country.name})"

class Office(models.Model):
    
    Building= models.ForeignKey(Building, on_delete=models.CASCADE,null=True, blank=False, related_name='offices')
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.Building.name}, {self.Building.area.name}, {self.Building.area.governate.name}, {self.Building.area.governate.country.name})"


class AssetCount(models.Model):
    startDate = models.DateField(default=timezone.now)
    name = models.CharField(max_length=255,null=True,blank=False)
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Asset(models.Model):
    
    assetTag = models.CharField(max_length=255)
    office = models.ForeignKey(Office, on_delete=models.CASCADE,null=True, blank=False, related_name='asset')
    assetCount = models.ForeignKey(AssetCount, on_delete=models.CASCADE,null=False, blank=False, related_name='asset')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('assetTag', 'assetCount')

    def __str__(self):
        return self.assetTag
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Configuration Model
class Configuration(SingletonModel):  # Inherit from SingletonModel
    start_num = models.IntegerField(default=0)
    end_num = models.IntegerField(default=1)

    def clean(self):
        if self.start_num < 0:
            raise ValidationError('Start number cannot be negative.')
        if self.end_num < 0:
            raise ValidationError('End number cannot be negative.')
        if self.start_num >= self.end_num:
            raise ValidationError('Start number cannot be greater than or equal to the end number.')

    def update_start_num(self, quantity):
        if self.start_num + quantity <= self.end_num:
            self.start_num += quantity
            self.save()
        else:
            raise ValidationError('Quantity must be within the configuration range.')

    def __str__(self):
        return f"Configuration (Start: {self.start_num}, End: {self.end_num})"
    

class Images(models.Model):
    barcode = models.ForeignKey('Barcode', on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='barcodes/')

    def __str__(self):
        return f"{self.barcode} ({self.image_path})"
    
@receiver(post_delete, sender= Images )
def delete_barcode_image(sender, instance, **kwargs):
    if instance.image_path:
        if os.path.isfile(instance.image_path.path):
            os.remove(instance.image_path.path)


class Barcode(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    configuration = models.ForeignKey('Configuration', on_delete=models.CASCADE)

    @property
    def start_num(self):
        return self.configuration.start_num if self.configuration else 'N/A'

    @property
    def end_num(self):
        return self.configuration.end_num if self.configuration else 'N/A'

    def clean(self):
        if not self.configuration:
            raise ValidationError('No configuration selected.')

        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than zero.')

        if self.quantity > self.configuration.end_num:
            raise ValidationError('Quantity must be within the range defined by the configuration.')

    def generate_barcodes(self):
        barcodes = []
        start_num = self.configuration.start_num
        end_num = self.configuration.end_num

        for i in range(self.quantity):
            num = start_num + i
            if num > end_num:
                break
            code = f'{self.category.code}-{num}'
            barcodes.append(code)
            self.save_barcode_image(code)
        return barcodes

    def save_barcode_image(self, code):
        output_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
        os.makedirs(output_dir, exist_ok=True)
        file_name = f'{code}.png'
        file_path = os.path.join(output_dir, file_name)

        barcode = Code128(code, writer=ImageWriter())
        image = barcode.render()

        image = image.resize((int(2 * 96), int(1 * 96)), Image.Resampling.LANCZOS)
        image.save(file_path)

        # Save only the relative path to the Images model
        image_instance = Images(barcode=self, image_path=os.path.join('barcodes', file_name))
        image_instance.save()


    def save(self, *args, **kwargs):
        self.clean()  # Validate model instance
        super().save(*args, **kwargs)  # Save the Barcode instance
        # Ensure the configuration is available before saving
        config = Configuration.objects.first()
        if not config:
            raise ValueError('No configuration found.')

        # Update configuration if necessary
        if self.quantity <= config.end_num:
            config.update_start_num(self.quantity)
        # Generate barcodes and save images
        self.generate_barcodes()

    def __str__(self):
        return f"{self.category} ({self.quantity})"