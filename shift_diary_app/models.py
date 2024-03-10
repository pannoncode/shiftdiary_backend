from django.db import models


# Create your models here.

"""
Gép (amihez később műszaknaplót lehet rendelni) létrehozásához szükséges modellek
"""


class MachineModel(models.Model):
    """Új gép - Alap géptulajdonságok, sebesség, termelékenység, oee célok"""
    machine_name_or_number = models.CharField(max_length=100, unique=True)
    machine_speed = models.IntegerField()
    max_product_volume_per_min = models.IntegerField()
    shift_time_min = models.IntegerField()
    oee_target = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.machine_name_or_number

    def max_product_volume_per_shift(self):
        return self.shift_time_min * self.max_product_volume_per_min


class ProductToMachineModel(models.Model):
    """Termékhez rendelt gép, esetleg módosított sebesség (csak opció a jövőben)"""
    machine = models.ForeignKey(
        MachineModel, on_delete=models.CASCADE)
    product_number = models.IntegerField(null=True)
    product_name = models.CharField(max_length=100)
    one_piece_weight = models.DecimalField(
        max_digits=20, decimal_places=4, null=True)
    prod_num_in_mc = models.IntegerField(null=True)
    modified_machine_speed = models.IntegerField()
    modified_product_volume_per_min = models.IntegerField()

    def __str__(self) -> str:
        return str(self.machine) + " " + self.product_name

    def modified_product_volume_per_shift(self):
        return self.machine.shift_time_min * self.modified_product_volume_per_min


class ProductsModel(models.Model):
    """Termelhető termékek"""
    product_number = models.IntegerField()
    product_name = models.CharField(max_length=255)
    one_piece_weight = models.DecimalField(
        max_digits=20, decimal_places=4)  # selejt számoláshoz kell
    prod_num_in_mc = models.IntegerField(null=True)

    def __str__(self) -> str:
        return str(self.product_number) + " - " + self.product_name


"""
Műszaknapló létrehozásához szükséges modellek
"""


class ShiftDiaryModel(models.Model):
    """Műszaknapló - kitöltő neve, dátum, műszak, gépszám, kapcsolat a többi modellel"""
    created = models.DateField(auto_now=True)
    created_it = models.CharField(max_length=50)
    shift_date = models.DateField(auto_now=False)
    shift = models.CharField(max_length=20)
    machine_number = models.ForeignKey(MachineModel, on_delete=models.CASCADE)
    # production_volume = models.ForeignKey(
    #     ProductionVolumeModel, related_name="production", on_delete=models.CASCADE)
    complated = models.CharField(max_length=20, default="edit")
    user_id = models.IntegerField()

    def __str__(self) -> str:
        return str(self.machine_number) + " " + str(self.created_it)


class SafetyModel(models.Model):
    """Biztonság - baleset, észrevételek"""
    shift_diary = models.OneToOneField(
        ShiftDiaryModel, on_delete=models.CASCADE, related_name='safety')
    accident_num = models.IntegerField(null=True)
    accident = models.CharField(max_length=255)
    safety_notes = models.CharField(max_length=255)
    created = models.DateField(auto_now=True)
    created_it = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.shift_diary) + " " + "biztonság"


class QualityModel(models.Model):
    """Minőség - minőségi hibák, észrevételek"""
    shift_diary = models.OneToOneField(
        ShiftDiaryModel, on_delete=models.CASCADE, related_name='quality')
    minor_qa_defect_num = models.IntegerField(null=True)
    minor_qa_defect = models.CharField(max_length=100)
    major_qa_defect_num = models.IntegerField(null=True)
    major_qa_defect = models.CharField(max_length=100)
    quality_notes = models.CharField(max_length=255)
    created = models.DateField(auto_now=True)
    created_it = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.shift_diary) + " " + "minőség"


class EmployeesModel(models.Model):
    """Létszám - sori létszám, jelenlévők, táppénzen lévők ...stb"""
    shift_diary = models.OneToOneField(
        ShiftDiaryModel, on_delete=models.CASCADE, related_name='employees')
    full_line_manpower = models.IntegerField()
    staff_present = models.IntegerField()
    staff_sick_pay_num = models.IntegerField()
    staff_sick_pay = models.CharField(max_length=100)
    staff_holiday_num = models.IntegerField()
    staff_holiday = models.CharField(max_length=100)
    staff_unverified_num = models.IntegerField()
    staff_unverified = models.CharField(max_length=100)
    staff_notes = models.CharField(max_length=255)
    created = models.DateField(auto_now=True)
    created_it = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.shift_diary) + " " + "létszám"


class MachineDefectModel(models.Model):
    """Géphibák - rövidebb-hosszabb állások, géppel kapcsolatos megjegyzések"""
    shift_diary = models.OneToOneField(
        ShiftDiaryModel, on_delete=models.CASCADE, related_name='machinedefects')
    longer_stops_num = models.IntegerField()
    longer_stops = models.CharField(max_length=255)
    minor_stops_num = models.IntegerField()  # ez egy lehetőség ha lenne rá szükség
    minor_stops = models.CharField(max_length=255)  # ezt már érdemes használni
    machine_defect_notes = models.CharField(max_length=255)
    created = models.DateField(auto_now=True)
    created_it = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.shift_diary) + " " + "géphibák"


class ProductionVolumeModel(models.Model):
    """Termelt mennyiségek - tervezett és termelt mennyiségek"""
    shift_diary = models.ForeignKey(
        ShiftDiaryModel, on_delete=models.CASCADE, related_name="volumes")
    """
    OneToOneField-el egy terméket csak egyszer lehet beírni!!!
    """
    product = models.ForeignKey(
        ProductsModel, on_delete=models.CASCADE, related_name="production_volume")
    product_order = models.IntegerField()
    planned_volume = models.DecimalField(max_digits=20, decimal_places=4)
    product_volume = models.DecimalField(max_digits=20, decimal_places=4)
    plan_fulfillment = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    created = models.DateField(auto_now=True)
    created_it = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.shift_diary) + " " + str(self.product_order) + " " + "termelt mennyiségek"
