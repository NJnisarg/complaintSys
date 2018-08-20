from django.urls import path
from .views import *

urlpatterns = [
    path('get_all_complaints/', get_all_complaints, name='get_all_complaints'),
    path('get_complaint/<pk>/', get_complaint, name='get_complaint'),
    path('get_comp_by_user/<pk>/', get_complaint_by_complainant, name='get_complaint_by_user'),
    path('get_comp_by_tag/<pk>/', get_complaint_by_tags, name='get_complaint_by_tags'),
    path('get_complaint_unresolved/', get_complaint_unresolved, name='get_complaint_unresolved'),
    path('get_complaint_resolved/', get_complaint_resolved, name='get_complaint_resolved'),
    path('create_tag/', create_tag, name='create_tag'),
    path('get_all_tags/', get_all_tags, name='get_all_tags'),
    path('generate_complaint/', generate_complaint, name='generate_complaint'),
    path('update_complaint_data/<pk>/', update_complaint_data, name='update_complaint_data'),
    path('resolve_complaint/<pk>/', resolve_complaint, name='resolve_complaint'),
    path('add_comment/<pk>/', add_comment_to_complaint, name='add_complaint'),
]
