from rest_framework import serializers
from .models import (MachineModel,
                     ProductToMachineModel,
                     ProductsModel,
                     SafetyModel,
                     QualityModel,
                     EmployeesModel,
                     MachineDefectModel,
                     ProductionVolumeModel,
                     ShiftDiaryModel
                     )

"""
Gépek létrehozására
"""


class MachineSerializer(serializers.ModelSerializer):
    max_product_volume_per_shift = serializers.SerializerMethodField()

    def get_max_product_volume_per_shift(self, obj):
        return obj.max_product_volume_per_shift()

    class Meta:
        model = MachineModel
        fields = "__all__"


class ProductToMachineSerializer(serializers.ModelSerializer):
    modified_product_volume_per_shift = serializers.SerializerMethodField()

    def get_modified_product_volume_per_shift(self, obj):
        return obj.modified_product_volume_per_shift()

    class Meta:
        model = ProductToMachineModel
        fields = "__all__"


"""
Új termék létrehozására
"""


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsModel
        fields = "__all__"


"""
Műszaknaplók létrehozására
"""


class SafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyModel
        fields = "__all__"


class QualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityModel
        fields = "__all__"


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeesModel
        fields = "__all__"


class MachineDefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineDefectModel
        fields = "__all__"


class ProductionVolumeSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductsModel.objects.all(),
        source='product',
        write_only=True
    )
    class Meta:
        model = ProductionVolumeModel
        fields = "__all__"


class ShiftDiarySerializer(serializers.ModelSerializer):
    machine_number = MachineSerializer(read_only=True)
    machine_number_id = serializers.PrimaryKeyRelatedField(
        queryset=MachineModel.objects.all(),
        source='machine_number',
        write_only=True
    )
    safety = SafetySerializer(read_only=True)
    quality = QualitySerializer(read_only=True)
    employees = EmployeesSerializer(read_only=True)
    machinedefects = MachineDefectSerializer(read_only=True)
    volumes = ProductionVolumeSerializer(read_only=True, many=True)

    class Meta:
        model = ShiftDiaryModel
        fields = "__all__"
