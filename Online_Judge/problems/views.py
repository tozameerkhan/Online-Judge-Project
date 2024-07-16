from django.shortcuts import render,redirect, get_object_or_404
from .models import Problem
from .forms import ProblemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


# Create your views here.
@login_required
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problem_list.html', {'problems': problems})

@login_required
def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)  # Create instance but don't save to DB yet
            problem.user = request.user  # Assign the current authenticated user
            problem.save()  # Now save the instance with user assigned
            return redirect('/problem/all_problem')  # Redirect to problem list page after creation
    else:
        form = ProblemForm()
    
    return render(request, 'problem_form.html', {'form': form})

'''@login_required
def update_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            return redirect('/problem/all_problem')  # Redirect to problem list page after update
    else:
        form = ProblemForm(instance=problem)
    
    return render(request, 'problem_form.html', {'form': form})
'''




@login_required
def update_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    
    # Check if the current user is the creator of the problem or an admin
    if problem.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to update this problem.')
        return redirect('problems:problem_list')  # Redirect to problem list page
    
    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            messages.info(request, 'Problem updated.')
            return redirect('/problem/all_problem')  # Redirect to problem list page after update
    else:
        form = ProblemForm(instance=problem)
    
    return render(request, 'problem_update_form.html', {'form': form})



@login_required
def delete_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    # Check if the current user is the creator of the problem or an admin
    if problem.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this problem.')
        return redirect('problems:problem_list')  # Redirect to problem list page
    
    if request.method == 'POST':
        problem.delete()
        messages.info(request, 'Problem deleted.')
        return redirect('/problem/all_problem')  # Redirect to problem list page after deletion
    
    return render(request, 'problem_confirm_delete.html', {'problem': problem})


@login_required
def solve_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    if request.method == 'POST':
        # Handle the form submission for code execution or problem submission
        # This part will be expanded later to handle the actual code running logic
        user_code = request.POST.get('code')
        user_input = request.POST.get('user_input')

        # You can add logic here to execute the code and capture the output
        result = run_user_code(user_code, user_input)

        return render(request, 'solve_problem.html', {
            'problem': problem,
            'user_code': user_code,
            'user_input': user_input,
            'result': result,
        })

    return render(request, 'solve_problem.html', {'problem': problem})


def run_user_code(code, user_input):
    # Implement this function to run user code and return the result
    # This can be done using subprocess in Python or any other method
    # For now, we'll return a placeholder value
    return "Execution result will be shown here."
