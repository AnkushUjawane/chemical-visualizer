from rest_framework import serializers
from .models import EquipmentDataset, Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['name', 'type', 'flowrate', 'pressure', 'temperature']

class EquipmentDatasetSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'filename', 'uploaded_at', 'total_count', 'avg_flowrate', 
                  'avg_pressure', 'avg_temperature', 'type_distribution', 'equipment']
