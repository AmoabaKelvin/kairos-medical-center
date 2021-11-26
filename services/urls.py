from django.urls import path
from . import views

urlpatterns = [
    path('addtest/', views.AddTestView.as_view(), name='add_test'),
    path('edittest/<int:pk>', views.EditTestView.as_view(), name='edit_test'),
    path('listtests/', views.LabTestsListView.as_view(), name='list_tests'),
    path('delete/<int:pk>', views.delete_test, name='delete_test'),
    path('search/', views.search_for_test, name='search_test'),
]