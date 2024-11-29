# urls.py
from django.urls import path
from . import views
app_name="connection"
urlpatterns = [
    path('', views.laboratory_selection, name='laboratory_selection'),
    path('laboratory/<int:lab_id>/', views.manage_laboratory, name='manage_laboratory'),
    path('toggle_computer/<int:computer_id>/<str:action>/', views.toggle_computer, name='toggle_computer'),
    path("toggle_all/<int:laboratory_id>/<str:action>/", views.toggle_all_computers, name="toggle_all_computers"),
]
