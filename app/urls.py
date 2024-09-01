from django.urls import path
from . import views
from . views import *

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/alerts/', views.alert_log_list, name='alert_log_list'),
    path('config/', config_list, name='config-list'),
    path('config/create/', config_create, name='config-create'),
    path('config/<int:pk>/update/', config_update, name='config-update'),
    path('config/<int:pk>/delete/', config_delete, name='config-delete'),
    
    path('api/record/', record_data, name='record-data'),
    
    path('report/', report_view, name='report-view'),
    path('report_data/', report_data, name='report-data'),
    path('download_report/', download_report, name='download-report'),
    
    path('update_stage/', update_stage, name='update-stage'),
    path('serial-data/', serial_data_view, name='serial-data'),
    
    path('logs/', alert_log_data, name='alert_log_data')
]