from io import BytesIO
import uuid
from django.db import models
from django.dispatch import receiver
from django.forms import ValidationError
from django.utils import timezone
from barcode import Code128
from barcode.writer import ImageWriter
import os
from django.conf import settings
from django.db.models.signals import post_delete
from solo.models import SingletonModel
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display
import arabic_reshaper

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

    @property
    def start_num(self):
        return Configuration.get_solo().start_num

    @property
    def end_num(self):
        return Configuration.get_solo().end_num

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than zero.')

        if self.quantity > self.end_num:
            raise ValidationError('Quantity must be within the range defined by the configuration.')

    def generate_barcodes(self):
        barcodes = []
        start_num = self.start_num
        end_num = self.end_num

        for i in range(self.quantity):
            num = start_num + i
            if num > end_num:
                break
            code = f'{self.category.code}-{num}'
            barcodes.append(code)
            self.save_barcode_image(code)
        return barcodes

    def save_barcode_image(self, code):
        # Define output directory and file path
        output_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
        os.makedirs(output_dir, exist_ok=True)
        file_name = f'{code}.png'
        file_path = os.path.join(output_dir, file_name)

        # Generate the barcode image
        barcode = Code128(code, writer=ImageWriter())
        barcode_image = barcode.render()

        # Resize barcode to fit within 2x1 inches (192x96 pixels at 96 DPI)
        barcode_image = barcode_image.resize((600,295))

        # Create a blank image of size 2x1 inches
        final_image = Image.new('RGB', (600,295), 'white')

        # Add the barcode to the blank image
        final_image.paste(barcode_image, (0, int(0.2 * 96)))  # Paste barcode slightly lower

        # Add text above the barcode
        # Add text above the barcode
        draw = ImageDraw.Draw(final_image)

        # Reverse and reshape the Arabic part of the text
        english_text = self.category.name
        arabic_text = arabic_reshaper.reshape(self.category.name_ar)
        bidi_text = get_display(arabic_text)

        # Combine the English and reshaped Arabic text
        text = f'{english_text} - {bidi_text}'
        font_size = 20  # Adjust font size as needed

        try:
            font = ImageFont.truetype("arial.ttf", font_size)  # Use a TrueType font
        except IOError:
            font = ImageFont.load_default()  # Fallback to default font if TrueType font is not found

        # Calculate text size using the bounding box
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculate the position to center the text
        text_x = (final_image.width - text_width) // 2  # Center the text horizontally
        text_y = (int(0.2 * 96) - text_height) // 2    # Place text above the barcode
        
        # Draw the text onto the image
        draw.text((text_x, text_y), text, fill="black", font=font)

        # Save the final image
        final_image.save(file_path)

        # Save only the relative path to the Images model
        image_instance = Images(barcode=self, image_path=os.path.join('barcodes', file_name))
        image_instance.save()

    def save(self, *args, **kwargs):
        self.clean()  # Validate model instance
        super().save(*args, **kwargs)  # Save the Barcode instance

        # Ensure the configuration is available before saving
        config = Configuration.get_solo()
        if not config:
            raise ValueError('No configuration found.')

        # Update configuration if necessary
        if self.quantity <= config.end_num:
            config.update_start_num(self.quantity)
        
        # Generate barcodes and save images
        self.generate_barcodes()

    def __str__(self):
        return f"{self.category} ({self.quantity})"