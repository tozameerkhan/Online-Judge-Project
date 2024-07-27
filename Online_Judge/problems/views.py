from django.shortcuts import render,redirect, get_object_or_404
from .models import Problem, TestCase
from .forms import ProblemForm, ProblemUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import CodeSubmissionForm, TestCaseForm
from django.conf import settings
import uuid
import subprocess
from pathlib import Path
from django.urls import reverse

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

            # Save hidden test cases if they are provided
            hidden_input = form.cleaned_data.get('hidden_input', '')
            hidden_output = form.cleaned_data.get('hidden_output', '')

            if hidden_input and hidden_output:
                TestCase.objects.create(
                    problem=problem,
                    input_data=hidden_input,
                    output_data=hidden_output,
                    hidden=True
                )
            return redirect('/problem/all_problem')  # Redirect to problem list page after creation
    else:
        form = ProblemForm()
    
    return render(request, 'problem_form.html', {'form': form})




@login_required
def update_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    
    # Check if the current user is the creator of the problem or an admin
    if problem.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to update this problem.')
        return redirect('problems:problem_list')  # Redirect to problem list page
    
    if request.method == 'POST':
        form = ProblemUpdateForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()

            messages.info(request, 'Problem updated.')
            return redirect('/problem/all_problem')  # Redirect to problem list page after update
    else:
        form = ProblemUpdateForm(instance=problem)
    
    return render(request, 'problem_update_form.html', {'form': form})




@login_required
def delete_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    # Check if the current user is the creator of the problem or an admin
    if problem.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this problem.')
        return redirect('problems:problem_list')  # Redirect to problem list page
    
    if request.method == 'POST':
        # Delete all test cases related to the problem
        TestCase.objects.filter(problem=problem).delete()
        problem.delete()
        messages.info(request, 'Problem deleted.')
        return redirect('/problem/all_problem')  # Redirect to problem list page after deletion
    
    return render(request, 'problem_confirm_delete.html', {'problem': problem})



'''
@login_required
def solve_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    form = CodeSubmissionForm(request.POST or None)
    result = None

    if request.method == 'POST':
        if form.is_valid():
            code = form.cleaned_data['code']
            language = form.cleaned_data['language']
            user_input = form.cleaned_data['input_data']
            action = request.POST.get('action')

            if action == 'run':
                #if user_input:
                    result = run_user_code(language, code, user_input)  # Your function to run code with user input
                #else:
                    #messages.error(request, 'Please provide input to run the code.')

            elif action == 'submit':
                hidden_test_cases = TestCase.objects.filter(problem=problem)
                all_passed = True
                for test_case in hidden_test_cases:
                    expected_output = test_case.output_data
                    messages.error(request, f'out {expected_output} and {test_case.input_data}' )
                    actual_output = run_user_code(language, code, test_case.input_data)
                    if actual_output.strip() != expected_output.strip():
                        all_passed = False
                        result = f'Test case failed. Expected: {expected_output}, but got: {actual_output}'
                        break
                if all_passed:
                    result = 'All test cases passed!'
                else:
                    messages.error(request, result)
    
    context = {
        'problem': problem,
        'form': form,
        'result': result,
    }
    return render(request, 'solve_problem.html', context)
'''


login_required
def solve_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    result = None

    initial_code_templates = {
        'cpp': '#include <iostream>\nusing namespace std;\n\nint main() {\n    // Your code here\n    return 0;\n}',
        'c': '#include <stdio.h>\n\nint main() {\n    // Your code here\n    return 0;\n}',
        'py': '# Your Python code here'
    }

    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST or None)
        if form.is_valid():
            submission = form.save()
            code = submission.code
            language = submission.language
            user_input = submission.input_data
            action = request.POST.get('action')

            if action == 'run':
                    result = run_user_code(language, code, user_input)  #function to run code with user input

            elif action == 'submit':
                hidden_test_cases = TestCase.objects.filter(problem=problem)
                all_passed = True
                for test_case in hidden_test_cases:
                    expected_output = test_case.output_data
                    #messages.error(request, f'out {expected_output} and {test_case.input_data}' )
                    actual_output = run_user_code(language, code, test_case.input_data)
                    if actual_output.strip() != expected_output.strip():
                        all_passed = False
                        result = f'Test case failed. For input: {test_case.input_data}. Expected: {expected_output}, but got: {actual_output}'
                        break
                if all_passed:
                    result = 'All test cases passed!'
                    # Increase the number of problems solved by the user
                    user_profile = request.user.userprofile
                    user_profile.problems_solved += 1
                    user_profile.save()

    else:
        form = CodeSubmissionForm()
        selected_language = form.initial.get('language', 'cpp')  # Default to Python
        form.initial['code'] = initial_code_templates.get(selected_language, '')

    context = {
        'problem': problem,
        'form': form,
        'result': result,
    }
    return render(request, 'solve_problem.html', context)





def run_user_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    with open(output_file_path, "w") as output_file:
        pass  # This will create an empty file

    try:
        if language == "cpp":
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ["clang++", str(code_file_path), "-o", str(executable_path)],
                stderr=subprocess.PIPE,  # Capture stderr
            )

            if compile_result.returncode != 0:
                error_message = compile_result.stderr.decode("utf-8").strip()
                return f"Compilation Error:\n{error_message}"
            
            if compile_result.returncode == 0:
                with open(input_file_path, "r") as input_file:
                    with open(output_file_path, "w") as output_file:
                        subprocess.run(
                            [str(executable_path)],
                            stdin=input_file,
                            stdout=output_file,
                        )
        elif language == "py":
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    run_result = subprocess.run(
                        ["python3", str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,  # Capture stderr
                    )
                    if run_result.returncode != 0:
                        error_message = run_result.stderr.decode("utf-8").strip()
                        return f"Runtime Error:\n{error_message}"
                    
    except subprocess.CalledProcessError as e:
        return f"Runtime Error:\n{e}"

    # Read the output from the output file
    with open(output_file_path, "r") as output_file:
        output_data = output_file.read()

    return output_data



@login_required
def view_test_cases(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    # Check if the current user is the creator of the problem or an admin
    if problem.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to open this.')
        return redirect('problems:problem_list')  # Redirect to problem list page
    
    test_cases = TestCase.objects.filter(problem=problem)

    context = {
        'problem': problem,
        'test_cases': test_cases,
    }
    return render(request, 'view_test_cases.html', context)



@login_required
def add_test_case(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    # Check if the current user is the creator of the problem or an admin
    if problem.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to add test case.')
        return redirect('problems:problem_list')  # Redirect to problem list page
    

    if request.method == 'POST':
        form = TestCaseForm(request.POST)
        if form.is_valid():
            test_case = form.save(commit=False)
            test_case.problem = problem
            test_case.save()
            messages.success(request, 'Test case added successfully.')
            return redirect('problems:view_test_cases', pk=problem.id)  # Redirect to view test cases page
    else:
        form = TestCaseForm()

    context = {
        'form': form,
        'problem': problem,
    }
    return render(request, 'add_test_case.html', context)




@login_required
def update_test_case(request, pk):
    test_case = get_object_or_404(TestCase, pk=pk)
    problem = test_case.problem
    # Check if the current user is the creator of the problem or an admin
    if problem.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to update test case.')
        return redirect('problems:problem_list')  # Redirect to problem list page
    
    if request.method == 'POST':
        form = TestCaseForm(request.POST, instance=test_case)
        if form.is_valid():
            form.save()
            messages.info(request, 'Test Case updated.')
            url = f'/problem/{problem.pk}/view-test-cases/'  # Redirect to view test cases page
            return redirect(url)
    else:
        form = TestCaseForm(instance=test_case)

    context = {
        'form': form,
        'problem': problem,
        'test_case': test_case,
    }
    return render(request, 'update_test_case.html', context)



@login_required
def delete_test_case(request, pk):
    test_case = get_object_or_404(TestCase, pk=pk)
    problem = test_case.problem
    # Check if the current user is the creator of the problem or an admin
    if problem.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete test case.')
        return redirect('problems:problem_list')  # Redirect to problem list page
    
    if request.method == 'POST':
        problem_pk = test_case.problem.pk
        test_case.delete()
        messages.info(request, 'Test case deleted.')
        return redirect('problems:view_test_cases', pk=problem_pk)
    
    return render(request, 'delete_test_case.html', {'test_case': test_case})
