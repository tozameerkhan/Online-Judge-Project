from django.urls import path
from problems.views import problem_list, update_problem, create_problem, delete_problem, solve_problem, add_test_case, view_test_cases, update_test_case, delete_test_case

app_name = 'problems'

urlpatterns = [
    path('all_problem/', problem_list, name='problem_list'),
    path('create/', create_problem, name='create_problem'),
    path('<int:pk>/update/', update_problem, name='update_problem'),
    path('<int:pk>/delete/', delete_problem, name='delete_problem'),
    path('<int:problem_id>/', solve_problem, name='solve_problem'),
    path('<int:problem_id>/add_test_case/', add_test_case, name='add_test_case'),
    path('<int:pk>/view-test-cases/', view_test_cases, name='view_test_cases'),
    path('update-test-case/<int:pk>/', update_test_case, name='update_test_case'),
    path('delete-test-case/<int:pk>/', delete_test_case, name='delete_test_case'),

]
