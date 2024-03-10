from django.urls import path
from .views import (MachineView,
                    ProductToMachineView,
                    ProductsView,
                    ShiftDiaryView,
                    SafetyView,
                    QualityView,
                    EmployeesView,
                    MachineDefectView,
                    ProductionVolumeView,
                    SelectedShiftDiaryView,
                    DiaryView
                    )

urlpatterns = [
    path("new-machine/", MachineView.as_view(),
         name="new-machine"),
    path("new-machine/<int:pk>", MachineView.as_view(),
         name="delete-patch-machine"),
    path("new-machine-to-product/", ProductToMachineView.as_view(),
         name="new-machine-to-product"),

    path("products/", ProductsView.as_view(), name="create-edit-products"),
    path("products/<int:pk>", ProductsView.as_view(),
         name="create-edit-products"),

    path("new-shift-diary/", ShiftDiaryView.as_view(),
         name="new-shift-diary"),
    path("edit-shift-diary/<int:pk>", ShiftDiaryView.as_view(),
         name="edit-shift-diary"),

    path("safety-data/", SafetyView.as_view(), name="create-get-safety"),
    path("safety-data/<int:pk>", SafetyView.as_view(), name="edit-safety"),

    path("quality-data/", QualityView.as_view(), name="create-get-quality"),
    path("quality-data/<int:pk>", QualityView.as_view(), name="edit-quality"),

    path("employees-data/", EmployeesView.as_view(), name="create-get-employees"),
    path("employees-data/<int:pk>", EmployeesView.as_view(), name="edit-employees"),

    path("machine-defect-data/", MachineDefectView.as_view(),
         name="create-get-machine-defect"),

    path("machine-defect-data/<int:pk>", MachineDefectView.as_view(),
         name="create-get-machine-defect"),

    path("products-volume/", ProductionVolumeView.as_view(),
         name="create-get-product-volume"),
    path("products-volume/<int:pk>", ProductionVolumeView.as_view(),
         name="delete-product-volume"),
    path("selected-diary/", SelectedShiftDiaryView.as_view(), name="selected-diary"),
    path("diary/", DiaryView.as_view(), name="diary")
]
