from django.contrib import admin
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

# Register your models here.
admin.site.register(MachineModel)
admin.site.register(ProductToMachineModel)
admin.site.register(ProductsModel)
admin.site.register(SafetyModel)
admin.site.register(QualityModel)
admin.site.register(EmployeesModel)
admin.site.register(MachineDefectModel)
admin.site.register(ProductionVolumeModel)
admin.site.register(ShiftDiaryModel)
