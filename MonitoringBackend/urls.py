from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework import routers
import MonitoringBackend.views as views

router = routers.DefaultRouter()

router.register(
    r"monitoring-data-file",
    views.MonitoringDataFileViewSet,
    basename="monitoring-data-file",
)

urlpatterns = [
    path("", RedirectView.as_view(url="/api/")),
    path("api/", include(router.urls)),
    path("api/monitoring-data/", views.get_monitoring_data),
    path('admin/', admin.site.urls),

]
