from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import EquipmentDataset, Equipment
from .serializers import EquipmentDatasetSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=400)
    User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created successfully'})

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        return Response({'message': 'Login successful', 'username': username})
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)
    
    csv_file = request.FILES['file']
    try:
        df = pd.read_csv(csv_file)
        
        # Normalize column names (strip spaces, handle both formats)
        df.columns = df.columns.str.strip()
        
        # Check for both 'Equipment_Name' and 'Equipment Name'
        if 'Equipment Name' in df.columns:
            df.rename(columns={'Equipment Name': 'Equipment_Name'}, inplace=True)
        
        required_cols = ['Equipment_Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        if not all(col in df.columns for col in required_cols):
            return Response({'error': f'Invalid CSV format. Required columns: {required_cols}. Found: {list(df.columns)}'}, status=400)
        
        # Calculate statistics
        total_count = len(df)
        avg_flowrate = df['Flowrate'].mean()
        avg_pressure = df['Pressure'].mean()
        avg_temperature = df['Temperature'].mean()
        type_distribution = df['Type'].value_counts().to_dict()
        
        # Create dataset
        dataset = EquipmentDataset.objects.create(
            user=request.user,
            filename=csv_file.name,
            total_count=total_count,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature,
            type_distribution=type_distribution
        )
        
        # Create equipment records
        for _, row in df.iterrows():
            Equipment.objects.create(
                dataset=dataset,
                name=row['Equipment_Name'],
                type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            )
        
        # Keep only last 5 datasets
        old_datasets = EquipmentDataset.objects.filter(user=request.user)[5:]
        for ds in old_datasets:
            ds.delete()
        
        serializer = EquipmentDatasetSerializer(dataset)
        return Response(serializer.data, status=201)
    
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_datasets(request):
    datasets = EquipmentDataset.objects.filter(user=request.user)[:5]
    serializer = EquipmentDatasetSerializer(datasets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset(request, dataset_id):
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id, user=request.user)
        serializer = EquipmentDatasetSerializer(dataset)
        return Response(serializer.data)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf(request, dataset_id):
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id, user=request.user)
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        p.drawString(100, 750, f"Chemical Equipment Report - {dataset.filename}")
        p.drawString(100, 720, f"Upload Date: {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}")
        p.drawString(100, 690, f"Total Equipment: {dataset.total_count}")
        p.drawString(100, 660, f"Average Flowrate: {dataset.avg_flowrate:.2f}")
        p.drawString(100, 630, f"Average Pressure: {dataset.avg_pressure:.2f}")
        p.drawString(100, 600, f"Average Temperature: {dataset.avg_temperature:.2f}")
        
        y = 570
        p.drawString(100, y, "Equipment Type Distribution:")
        y -= 20
        for eq_type, count in dataset.type_distribution.items():
            p.drawString(120, y, f"{eq_type}: {count}")
            y -= 20
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{dataset_id}.pdf"'
        return response
    
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=404)
