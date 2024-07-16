from django.urls import path
from problems.views import problem_list, update_problem, create_problem, delete_problem, solve_problem

app_name = 'problems'

urlpatterns = [
    path('all_problem/', problem_list, name='problem_list'),
    path('create/', create_problem, name='create_problem'),
    path('<int:pk>/update/', update_problem, name='update_problem'),
    path('<int:pk>/delete/', delete_problem, name='delete_problem'),
    path('<int:problem_id>/', solve_problem, name='solve_problem'),

]
