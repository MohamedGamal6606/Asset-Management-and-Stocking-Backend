from .models import (
    Configuration,
    Country, 
    Governate, 
    Area, 
    Building,
    Images, 
    Office, 
    AssetCount, 
    Asset,
    Barcode,
    Category
    )
from django.http import HttpResponse
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import openpyxl
from django.db import models
from datetime import datetime
from import_export import resources
from import_export.admin import ImportExportModelAdmin
import os
from django.conf import settings
from django.urls import path, reverse
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin 

# Define resources for each model
class CountryResource(resources.ModelResource):
    class Meta:
        model = Country
        fields = ('id', 'name', 'created_on', 'updated_on')

class GovernateResource(resources.ModelResource):
    class Meta:
        model = Governate
        fields = ('id', 'name', 'country', 'created_on', 'updated_on')

class AreaResource(resources.ModelResource):
    class Meta:
        model = Area
        fields = ('id', 'name', 'governate', 'created_on', 'updated_on')

class BuildingResource(resources.ModelResource):
    class Meta:
        model = Building
        fields = ('id', 'name', 'area', 'created_on', 'updated_on')

class OfficeResource(resources.ModelResource):
    class Meta:
        model = Office
        fields = ('id', 'name', 'Building', 'created_on', 'updated_on')

class AssetCountResource(resources.ModelResource):
    class Meta:
        model = AssetCount
        fields = ('id', 'name', 'startDate', 'created_on', 'updated_on')

class AssetResource(resources.ModelResource):
    class Meta:
        model = Asset
        fields = ('id', 'assetTag', 'office', 'assetCount', 'created_on', 'updated_on')

# Custom export to Excel
def export_as_excel(modeladmin, request, queryset):
    # Create an in-memory workbook and worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = modeladmin.model._meta.verbose_name_plural.capitalize()

    # Add headers
    headers = [field.verbose_name for field in modeladmin.model._meta.fields]
    worksheet.append(headers)

    # Add data rows
    for obj in queryset:
        row = []
        for field in modeladmin.model._meta.fields:
            value = getattr(obj, field.name)

            # Check if value is a related object and convert to a string
            if isinstance(value, models.Model):
                value = str(value)

            # Check if the value is a datetime or date object and strip timezone info
            if isinstance(value, (datetime,)):
                value = value.replace(tzinfo=None)  # Remove timezone info

            row.append(value)
        worksheet.append(row)

    # Prepare the response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={modeladmin.model._meta.verbose_name_plural}.xlsx'

    # Save the workbook to the response
    workbook.save(response)
    return response

# Filters
class YearFilter(admin.SimpleListFilter):
    title = _('year')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = set([obj.created_on.year for obj in model_admin.model.objects.all()])
        return [(year, year) for year in years]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_on__year=self.value())
        return queryset

class MonthFilter(admin.SimpleListFilter):
    title = _('month')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        months = set([(obj.created_on.month, obj.created_on.strftime('%B')) for obj in model_admin.model.objects.all()])
        return sorted(months, key=lambda x: x[0])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_on__month=self.value())
        return queryset

class DayFilter(admin.SimpleListFilter):
    title = _('day')
    parameter_name = 'day'

    def lookups(self, request, model_admin):
        days = set([(obj.created_on.day, obj.created_on.strftime('%d %B')) for obj in model_admin.model.objects.all()])
        return sorted(days, key=lambda x: x[0])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_on__day=self.value())
        return queryset

# Admin for Country model
class CountryAdmin(ImportExportModelAdmin):
    resource_class = CountryResource
    list_display = ('name', 'created_on', 'updated_on')
    ordering = ('name','id',)
    search_fields = ('name',)
    list_filter = (YearFilter, MonthFilter, DayFilter)
    date_hierarchy = 'created_on'
    actions = [export_as_excel]

admin.site.register(Country, CountryAdmin)

# Admin for Governate model
class GovernateAdmin(ImportExportModelAdmin):
    resource_class = GovernateResource
    list_display = ('name', 'country', 'created_on', 'updated_on')
    ordering = ('name','id',)
    search_fields = ('name', 'country__name')
    list_filter = (YearFilter, MonthFilter, DayFilter)
    date_hierarchy = 'created_on'
    raw_id_fields = ("country",)
    actions = [export_as_excel]

admin.site.register(Governate, GovernateAdmin)

# Admin for Area model
class AreaAdmin(ImportExportModelAdmin):
    resource_class = AreaResource
    list_display = ('name', 'governate', 'created_on', 'updated_on')
    ordering = ('name','id',)
    search_fields = ('name', 'governate__name')
    list_filter = (YearFilter, MonthFilter, DayFilter)
    date_hierarchy = 'created_on'
    raw_id_fields = ("governate",)
    actions = [export_as_excel]

admin.site.register(Area, AreaAdmin)

# Admin for Building model
class BuildingAdmin(ImportExportModelAdmin):
    resource_class = BuildingResource
    list_display = ('name', 'area', 'created_on', 'updated_on')
    ordering = ('name','id',)
    search_fields = ('name', 'area__name')
    list_filter = (YearFilter, MonthFilter, DayFilter)
    date_hierarchy = 'created_on'
    raw_id_fields = ("area",)
    actions = [export_as_excel]

admin.site.register(Building, BuildingAdmin)

# Admin for Office model
class OfficeAdmin(ImportExportModelAdmin):
    resource_class = OfficeResource
    list_display = ('name', 'Building', 'created_on', 'updated_on')
    ordering = ('name','id',)
    search_fields = ('name', 'Building__name')
    list_filter = (YearFilter, MonthFilter, DayFilter)
    date_hierarchy = 'created_on'
    raw_id_fields = ("Building",)
    actions = [export_as_excel]

admin.site.register(Office, OfficeAdmin)

# Admin for AssetCount model
class AssetCountAdmin(ImportExportModelAdmin):
    resource_class = AssetCountResource
    list_display = ('name', 'startDate', 'created_on', 'updated_on')
    ordering = ('name','id',)
    search_fields = ('name', 'office__name')
    list_filter = (YearFilter, MonthFilter, DayFilter)
    date_hierarchy = 'created_on'
    actions = [export_as_excel]

admin.site.register(AssetCount, AssetCountAdmin)

# Admin for Asset model
class AssetAdmin(ImportExportModelAdmin):
    resource_class = AssetResource
    list_display = ('assetTag', 'office', 'assetCount', 'created_on', 'updated_on')
    ordering = ('assetTag','id',)
    search_fields = ('assetTag', 'office__name', 'assetCount__name')
    list_filter = (YearFilter, MonthFilter, DayFilter)
    date_hierarchy = 'created_on'
    raw_id_fields = ("assetCount", "office",)
    actions = [export_as_excel]

admin.site.register(Asset, AssetAdmin)

# Define resources for each model
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'name_ar', 'code')

class BarcodeResource(resources.ModelResource):
    class Meta:
        model = Barcode
        fields = ('id', 'category', 'quantity', 'start_num', 'end_num')

# Admin for Category model
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'name_ar', 'code')
    ordering = ('name', 'id')
    search_fields = ('name', 'name_ar', 'code')
    actions = [export_as_excel]

admin.site.register(Category, CategoryAdmin)

# Admin for Barcode model
class BarcodeAdmin(ImportExportModelAdmin):
    resource_class = BarcodeResource
    list_display = ('category', 'quantity', 'print_barcodes_button')
    ordering = ('id',)
    search_fields = ('category__name', 'quantity')
    raw_id_fields = ("category",)
    actions = [export_as_excel, 'print_barcodes']

    def get_readonly_fields(self, request, obj=None):
        if obj:  
            return ('category', 'quantity')
        return ()

    def print_barcodes_button(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">Print Barcodes</a>',
            reverse('admin:print_barcodes', args=[obj.pk])
        )
    print_barcodes_button.short_description = 'Print Barcodes'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('print-barcodes/<int:barcode_id>/', self.admin_site.admin_view(self.print_barcodes), name='print_barcodes'),
        ]
        return custom_urls + urls

    def print_barcodes(self, request, barcode_id):
        barcode = Barcode.objects.get(id=barcode_id)
        images = barcode.images_set.all()  # Retrieve related images

        # Create a print-only HTML response
        html = '''
        <html>
        <head>
            <style>
                @media print {
                    body {
                        margin: 0;
                        padding: 0;
                    }
                    img {
                        display: block;
                        width: auto;
                        height: auto;
                        margin: 0;
                        page-break-inside: avoid;
                    }
                }
            </style>
            <script>
                window.onload = function() {
                    window.print();
                }
            </script>
        </head>
        <body>
        '''
        for image in images:
            image_url = f'{settings.MEDIA_URL}{image.image_path}'
            html += f'<img src="{image_url}" alt="Barcode Image" />'
        html += '''
        </body>
        </html>
        '''

        return HttpResponse(html)
    
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'image_path')  # Adjust based on actual fields
    search_fields = ('barcode__category__name', 'image_path')

admin.site.register(Barcode, BarcodeAdmin)
admin.site.register(Images, ImagesAdmin)


@admin.register(Configuration)
class ConfigurationAdmin(SingletonModelAdmin):
    pass

