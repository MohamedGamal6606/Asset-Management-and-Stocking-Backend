
from myapp.models import (
    Asset,  
    AssetCount,
    Country,
    Governate,
    Area,
    Building,
    Office,
    Barcode,
    Category,
    Configuration,
)
from .serializers import (
    AssetSerializer,  
    AssetCountSerializer,
    CountrySerializer,
    BuildingSerializer,
    GovernateSerializer,
    OfficeSerializer,
    AreaSerializer,
    BarcodeSerializer,
    CategorySerializer,
    ConfigurationSerializer,
    )
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class ConfigurationViewSet(APIView):
    def get(self, request, *args, **kwargs):
        # Handle GET request to list assets
        configuration = Configuration.objects.all()
        serializer = ConfigurationSerializer(configuration, many=True)
        return Response(serializer.data)



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        })

class AssetViewSet(APIView):
    def get(self, request, *args, **kwargs):
        # Handle GET request to list assets
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Handle POST request to create a new asset
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(APIView):
    def get(self, request, *args, **kwargs):
        # Handle GET request to list all categories
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Handle POST request to create a new category
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BarcodeViewSet(APIView):
    def get(self, request, *args, **kwargs):
        # Handle GET request to list all barcodes
        barcodes = Barcode.objects.all()
        serializer = BarcodeSerializer(barcodes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Handle POST request to create a new barcode
        serializer = BarcodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetCountListView(APIView):
    def get(self, request):
        countries = AssetCount.objects.all()
        serializer = AssetCountSerializer(countries, many=True)
        return Response(serializer.data)
    

class CountryListView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)


class GovernateListView(APIView):
    def get(self, request):
        country_id = request.query_params.get('country')
        if country_id:
            governates = Governate.objects.filter(country_id=country_id)
        else:
            governates = Governate.objects.all()
        
        serializer = GovernateSerializer(governates, many=True)
        return Response(serializer.data)


class AreaListView(APIView):
    def get(self, request):
        governate_id = request.query_params.get('governate')
        if governate_id:
            areas = Area.objects.filter(governate_id=governate_id)
        else:
            areas = Area.objects.all()
        serializer = AreaSerializer(areas, many=True)
        return Response(serializer.data)

class BuildingListView(APIView):
    def get(self, request):
        area_id = request.query_params.get('area')
        if area_id:
            buildings = Building.objects.filter(area_id=area_id)
        else:
            buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

class OfficeListView(APIView):
    def get(self, request):
        building_id = request.query_params.get('building')
        if building_id:
            offices = Office.objects.filter(Building_id=building_id)
        else:
            offices = Office.objects.all()
        serializer = OfficeSerializer(offices, many=True)
        return Response(serializer.data)