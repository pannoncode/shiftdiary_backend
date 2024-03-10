from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from .models import (MachineModel,
                     ProductToMachineModel,
                     ProductsModel,
                     ShiftDiaryModel,
                     SafetyModel,
                     QualityModel,
                     EmployeesModel,
                     MachineDefectModel,
                     ProductionVolumeModel
                     )

from .serializers import (MachineSerializer,
                          ProductToMachineSerializer,
                          ProductsSerializer,
                          ShiftDiarySerializer,
                          SafetySerializer,
                          QualitySerializer,
                          EmployeesSerializer,
                          MachineDefectSerializer,
                          ProductionVolumeSerializer
                          )

# Create your views here.


class MachineView(APIView):
    """Új gép létrehozására, szerkesztésére és törlésére"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return MachineModel.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, format=None):
        machines = MachineModel.objects.all().order_by("machine_name_or_number")
        serializer = MachineSerializer(machines, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MachineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres létrehozás!"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Nem sikerült létrehozni! Lehet, hogy ez a gépszám már létezik",
                "error": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk, format=None):
        selected_machine = self.get_object(pk)
        selected_machine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, format=None):
        selected_machine = self.get_object(pk)
        serializer = MachineSerializer(
            selected_machine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres szerkesztés!"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Sikertelen szerkesztés!"},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductToMachineView(APIView):
    """Termék géphez rendelése --> nincs használatban"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        product_machine = ProductToMachineModel.objects.all()
        serializer = ProductToMachineSerializer(product_machine, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductToMachineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres létrehozás"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Nem sikerült létrehozni",
                "error": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return ProductsModel.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, format=None):
        products = ProductsModel.objects.all()
        serializer = ProductsSerializer(products, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Sikeres létrehozás"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "message": "Sikertelen létrehozás",
                "error": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk, format=None):
        selected_product = self.get_object(pk=pk)
        serializer = ProductsSerializer(
            selected_product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Sikeres változtatés"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "message": "Sikertelen változtatás",
                "error": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk, format=None):
        selected_product = self.get_object(pk=pk)
        selected_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShiftDiaryView(APIView):
    """Műszaknapló létrehozás és lekérése, szerkesztése"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return ShiftDiaryModel.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, format=None):
        shift_diaries = ShiftDiaryModel.objects.all()
        serializer = ShiftDiarySerializer(shift_diaries, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShiftDiarySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeresen létrjött a műszaknapló"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Nem sikerült létrehozni a műsszaknaplót",
                "error": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk, format=None):
        selected_diary = self.get_object(pk=pk)
        serializer = ShiftDiarySerializer(
            selected_diary, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres szerkesztés"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"Nem sikerült szerkeszteni"},
            status=status.HTTP_400_BAD_REQUEST
        )


class SafetyView(APIView):
    """Műszaknaplón beleül a Biztonság opció"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return SafetyModel.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, format=None):
        safety = SafetyModel.objects.all()
        serializer = SafetySerializer(safety, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SafetySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres mentés"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "message": "Nem sikerült menteni az adatokat",
                "error": serializer.error_messages
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk, format=None):
        selected_safety = self.get_object(pk=pk)
        serializer = SafetySerializer(
            selected_safety, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres szerkesztés"},
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "message": "Sikertelen szerkesztés!",
                "error": serializer.error_messages
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class QualityView(APIView):
    """Műszaknaplón belül a Minőség opció"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return QualityModel.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, format=None):
        quality = QualityModel.objects.all()
        serializer = QualitySerializer(quality, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QualitySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres mentés"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "message": "Nem sikerült menteni az adatokat",
                "error": serializer.error_messages
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk, format=None):
        print(request.data)
        selected_quality = self.get_object(pk=pk)
        serializer = QualitySerializer(
            selected_quality, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres szerkesztés"},
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "message": "Sikertelen szerkesztés!",
                "error": serializer.error_messages
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class EmployeesView(APIView):
    """Műszaknaplón belül a Létszám opció"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return EmployeesModel.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, format=None):
        employees = EmployeesModel.objects.all()
        serializer = EmployeesSerializer(employees, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmployeesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres mentés!"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Sikertelen mentés!",
                "error": serializer.error_messages

            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk, format=None):
        selected_employees = self.get_object(pk=pk)
        serializer = EmployeesSerializer(
            selected_employees, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"Sikeres szerkesztés!"},
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Sikertelen szerkesztés!",
                "error": serializer.error_messages
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class MachineDefectView(APIView):
    """Műszaknaplón belül a Géphibák opció"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return MachineDefectModel.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, format=None):
        machine_defect = MachineDefectModel.objects.all()
        serializer = MachineDefectSerializer(machine_defect, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MachineDefectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Sikeres mentés!"
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Sikertelen mentés!",
                "error": serializer.error_messages
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk, format=None):
        selected_machine_Defect = self.get_object(pk=pk)

        serializer = MachineDefectSerializer(
            selected_machine_Defect, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Sikeres szerkesztés!"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "message": "Sikertelen szerkesztés",
                "error": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductionVolumeView(APIView):
    """Termelt mennyiségek"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return ProductionVolumeModel.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, format=None):
        production = ProductionVolumeModel.objects.all()
        serializer = ProductionVolumeSerializer(production, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = ProductionVolumeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres mentés!"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "message": "Sikertelen mentés",
                "error": serializer.error_messages
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk, format=None):
        selected_product = self.get_object(pk=pk)
        selected_product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SelectedShiftDiaryView(APIView):
    """Dátum és gépszám alapján kiválasztott műszaknapló"""

    def get(self, request, format=None):
        shift_date = request.query_params["shift_date"]
        machine_number = request.query_params["machine_number"]

        diary = ShiftDiaryModel.objects.filter(
            shift_date=shift_date, machine_number=machine_number)
        serializer = ShiftDiarySerializer(diary, many=True)

        return Response(serializer.data)


class DiaryView(APIView):
    """Dátum, gépszám és műszak alapján vissza adja a műszaknapló adatait"""

    def get(self, request, format=None):
        shift_date = request.query_params["shift_date"]
        machine_number = request.query_params["machine_number"]
        shift = request.query_params["shift"]

        diary = ShiftDiaryModel.objects.filter(
            shift_date=shift_date, machine_number=machine_number, shift=shift)
        serializer = ShiftDiarySerializer(diary, many=True)

        return Response(serializer.data)
