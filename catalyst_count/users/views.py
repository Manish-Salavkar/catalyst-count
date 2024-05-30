from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import MyFileForm
from .models import Company
from django.conf import settings
from .utils import generate_random_filename
from io import TextIOWrapper
from rest_framework import generics
from rest_framework.response import Response
from .serializer import QueryParamsSerializer
from django.contrib.auth.models import User
import csv
import os

def home(request):
    return render(request, 'base.html')

def upload_data(request):
    form = MyFileForm()
    return render(request, 'upload_data.html', {'form': form})

@csrf_exempt
@require_POST
def upload_csv(request):
    if 'file' not in request.FILES:
        print("File not in request files")
        return JsonResponse({'error': 'No file found in request'}, status=400)
    
    uploaded_file = request.FILES['file']

    if 'temp_file_name' not in request.session:
        request.session['temp_file_name'] = generate_random_filename()

    temp_file_name = request.session['temp_file_name']
    temp_file_path = os.path.join(settings.BASE_DIR, 'users', 'files', temp_file_name)

    with open(temp_file_path, 'ab') as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)

    is_final_chunk = request.POST.get('is_final_chunk') == 'true'

    if is_final_chunk:
        with open(temp_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                company_data = {
                    'name': row['name'],
                    'domain': row['domain'],
                    'year_founded': row['year founded'],
                    'industry': row['industry'],
                    'size_range': row['size range'],
                    'locality': row['locality'],
                    'country': row['country'],
                    'linkedin_url': row['linkedin url'],
                    'current_employee_estimate': int(row['current employee estimate']),
                    'total_employee_estimate': int(row['total employee estimate'])
                }
                Company.objects.create(**company_data)

        os.remove(temp_file_path)
        del request.session['temp_file_name']

        print("Upload complete")
        return JsonResponse({'success': 'CSV data uploaded and committed successfully'})

    print("Upload ongoing")
    return JsonResponse({'status': 'Chunk received, upload ongoing'})

@csrf_exempt
@require_POST
def upload_csv_simple(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file found in request'}, status=400)
    
    uploaded_file = request.FILES['file']

    # Assuming uploaded_file is a CSV file, you can directly process it
    csv_text = TextIOWrapper(uploaded_file, encoding='utf-8')

    reader = csv.DictReader(csv_text)
    for row in reader:
        company_data = {
            'name': row.get('name',''),
            'domain': row.get('domain',''),
            'year_founded': row.get('year_founded',''),
            'industry': row.get('industry',''),
            'size_range': row.get('size_range',''),
            'locality': row.get('locality',''),
            'country': row.get('country',''),
            'linkedin_url': row.get('linkedin_url',''),
        }
        current_employee_estimate = row.get('current employee estimate')
        if current_employee_estimate:
            company_data['current_employee_estimate'] = int(current_employee_estimate)
        
        total_employee_estimate = row.get('total employee estimate')
        if total_employee_estimate:
            company_data['total_employee_estimate'] = int(total_employee_estimate)
            
        Company.objects.create(**company_data)

    return JsonResponse({'success': 'CSV data uploaded and objects created successfully'})


def query_builder(request):
    unique_industries = Company.objects.values_list('industry', flat=True).distinct()
    unique_localities = Company.objects.values_list('locality', flat=True).distinct()
    unique_countries = Company.objects.values_list('country', flat=True).distinct()

    unique_industries_title = [industry.title() if industry else None for industry in unique_industries]
    unique_countries_title = [country.title() if country else None for country in unique_countries]

    cities = []
    states = []

    for locality in unique_localities:
        if locality:
            city, state, country = [part.strip() for part in locality.split(',')]

            cities.append(city.title())
            states.append(state.title())
        else:
            cities.append(None)
            states.append(None)

    context = {
        'unique_industries': unique_industries_title,
        'cities': cities,
        'states': states,
        'unique_countries': unique_countries_title,
    }

    return render(request, 'builder.html', context)


class QueryBuilderAPIView(generics.ListAPIView):
    serializer_class = QueryParamsSerializer

    def get_queryset(self):
        queryset = Company.objects.all()

        params_serializer = self.serializer_class(data=self.request.query_params)
        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.validated_data

        filters = {}
        if params.get('keyword'):
            filters['name__icontains'] = params['keyword']
        if params.get('industry'):
            filters['industry__icontains'] = params['industry']
        if params.get('cities'):
            filters['locality__icontains'] = params['cities']
        if params.get('states'):
            filters['locality__icontains'] = params['states']
        if params.get('country'):
            filters['country__icontains'] = params['country']
        if params.get('year'):
            filters['year_founded'] = params['year']
        if params.get('employees_from'):
            filters['current_employee_estimate__gte'] = params['employees_from']
        if params.get('employees_to'):
            filters['current_employee_estimate__lte'] = params['employees_to']

        if filters:
            queryset = queryset.filter(**filters)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
def users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'users.html', context)