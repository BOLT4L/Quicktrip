from django.urls import path 
from .views import *
urlpatterns = [
    path('admin_dashboard/',Ad_dashboard.as_view(), name="admin_dashboard" ),
    path('subadmin_dashboard/', sub_dashboard.as_view(), name = "subadmin_dashboard"),
    path('delete/', delete, name = "delete")
]
