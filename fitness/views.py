from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm, PasswordChangeForm
from .models import CustomUser,UserDashboardMetric,MealPlans,MealLog,WorkoutLog,Workout
from .forms import SignUpForm, CustomUserForm,WorkoutLogForm,MealLogForm
from django.contrib.auth import login, authenticate,logout,update_session_auth_hash
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.views.generic import DetailView,ListView,DeleteView
from django.utils.timezone import now
from django.db.models import Sum
import json
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')  

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        custom_user_form = CustomUserForm(request.POST)

        if form.is_valid() and custom_user_form.is_valid():
            user = form.save()
            custom_user = custom_user_form.save(commit=False)
            custom_user.user = user
            custom_user.email = user.email

            # Explicitly set the activity foreign key
            activity = custom_user_form.cleaned_data.get('activity')
            custom_user.activity = activity

            custom_user.save()

            # Authenticate and login the user
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = SignUpForm()
        custom_user_form = CustomUserForm()

    return render(request, 'signup.html', {'form': form, 'custom_user_form': custom_user_form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  
        else:
            return render(request, 'home.html', {'form': form, 'login_failed': True})
    else:
        return render(request, 'home.html', {'form': AuthenticationForm()})
        
def user_logout(request):
    logout(request)
    return redirect('home')

class DashboardView(DetailView):
    model = UserDashboardMetric
    template_name = 'dashboard.html'
    context_object_name = 'dashboard_metric'

    def get_object(self):
        custom_user = CustomUser.objects.get(user=self.request.user)
        try:
            return UserDashboardMetric.objects.get(user=custom_user)
        except UserDashboardMetric.DoesNotExist:
            default_metric = UserDashboardMetric(
                user=custom_user,
                exercise_sessions=0,
                total_calories_consumed=0,
                average_daily_calories=0,
                average_daily_exercises=0
            )
            default_metric.save()  
            return default_metric
    def get_context_data(self, **kwargs):
        custom_user = CustomUser.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        today = now().date()
        
        meal_plan = context["Mealplan"] = MealPlans.objects.get(user=custom_user)
        
        workouts = WorkoutLog.objects.filter(user=custom_user).order_by('-date')
        
        meals = json.loads(meal_plan.meals) if meal_plan.meals else []
        context["meals"] = meals
        
        meal_logs = MealLog.objects.filter(user=custom_user).order_by('-date')
        
        meal_logs_paginator = Paginator(meal_logs, 5)  
        page = self.request.GET.get('meal_page')
        try:
            context['meal_logs'] = meal_logs_paginator.page(page)
        except PageNotAnInteger:
            context['meal_logs'] = meal_logs_paginator.page(1)
        except EmptyPage:
            context['meal_logs'] = meal_logs_paginator.page(meal_logs_paginator.num_pages)
        
        workout_logs_paginator = Paginator(workouts, 5) 
        page = self.request.GET.get('workout_page')
        try:
            context['workouts'] = workout_logs_paginator.page(page)
        except PageNotAnInteger:
            context['workouts'] = workout_logs_paginator.page(1)
        except EmptyPage:
            context['workouts'] = workout_logs_paginator.page(workout_logs_paginator.num_pages)
        
        calories_consumed_today = context['Calories_today'] = MealLog.objects.filter(
            user=custom_user, date=today
        ).aggregate(total_calories=Sum('calories_consumed'))['total_calories'] or 0
        
        workout_sessions_today = context['workout_sessions_today'] = WorkoutLog.objects.filter(
            user=custom_user, date=today
        ).count()
        
        for workout in context["workouts"]:
            if isinstance(workout.exercises_completed, str):
                workout.exercises_completed = json.loads(workout.exercises_completed)
        
        if meal_plan:
            remaining_calories = meal_plan.calories_goal - calories_consumed_today
            context["remaining_calories"] = remaining_calories
        else:
            context["remaining_calories"] = None

        return context


def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')  
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'home.html', {'form': form,'password_change_failed': True})
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'home.html', {'form': form})

    
class MealLogListView(ListView):
    model = MealLog
    template_name = 'meal_log_list.html'
    context_object_name = 'meal_logs'
    paginate_by = 10

    def get_queryset(self):
        custom_user = get_object_or_404(CustomUser, user=self.request.user)
        queryset = MealLog.objects.filter(user=custom_user).order_by('-date')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_plans'] = MealPlans.objects.all()
        return context


class WorkoutLogListView(ListView):
    model = WorkoutLog
    form_class = WorkoutLogForm
    template_name = 'workout_log_list.html'
    context_object_name = 'workout_logs'
    paginate_by = 10
    def get_queryset(self):
        custom_user = get_object_or_404(CustomUser, user=self.request.user)
        queryset = WorkoutLog.objects.filter(user=custom_user).order_by('-date')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workouts'] = Workout.objects.all()
        for workout in context["workout_logs"]:
            if isinstance(workout.exercises_completed, str):
                workout.exercises_completed = json.loads(workout.exercises_completed)

        return context


def add_workout_log(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  

            workout_id = data.get('workout')
            exercises_completed = data.get('exercises_completed')
            notes = data.get('notes')

            if not workout_id or not exercises_completed:
                return JsonResponse({'success': False, 'errors': {'exercises_completed': ['This field is required.']}})

            user = CustomUser.objects.get(user=request.user)

            workout_log = WorkoutLog(
                user=user, 
                workout_id=workout_id,
                exercises_completed=json.dumps(exercises_completed),  
                notes=notes
            )
            workout_log.save()
            return JsonResponse({'success': True, 'message': 'Workout log added successfully.'})

        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'CustomUser not found for this user.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

    
def workout_exercises(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    exercises = json.loads(workout.exercises) 
    return JsonResponse({'exercises': exercises})

def update_workout_log(request, pk):
    if request.method == 'POST':
        try:
            data = request.POST
            workout_id = data.get('workout')
            exercises_completed = data.getlist('exercises_completed')
            notes = data.get('notes', '')

            workout_log = WorkoutLog.objects.get(pk=pk)
            workout_log.workout = Workout.objects.get(id=workout_id)
            workout_log.exercises_completed = json.dumps(exercises_completed)  
            workout_log.notes = notes
            workout_log.save()

            return redirect('workout-logs')

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

class WorkoutLogDeleteView(DeleteView):
    model = WorkoutLog
    success_url = reverse_lazy('workout-logs')
    template_name = 'workout_log_confirm_delete.html'
    
    def get_queryset(self):
        custom_user = get_object_or_404(CustomUser, user=self.request.user)
        return WorkoutLog.objects.filter(user=custom_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workouts'] = Workout.objects.all()
        return context
    
class MealLogDeleteView(DeleteView):
    model = MealLog
    success_url = reverse_lazy('meal-logs')
    template_name = 'delete_meal_log.html'
    
    def get_queryset(self):
        custom_user = get_object_or_404(CustomUser, user=self.request.user)
        return MealLog.objects.filter(user=custom_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_plans'] = MealPlans.objects.all()
        return context
    
def meal_log_create(request):
    custom_user = CustomUser.objects.get(user=request.user)
    meal_plan = MealPlans.objects.filter(user=custom_user).first()

    if not meal_plan:
        return redirect('meal-logs')

    if request.method == 'POST':
        form = MealLogForm(request.POST)
        
        if form.is_valid():
            meal_log = form.save(commit=False)
            meal_log.user = custom_user
            meal_log.meal_plan = meal_plan
            meal_log.save()

            return redirect('meal-logs')  
    else:
        form = MealLogForm()

    return render(request, 'meal_log_list.html', {'form': form})

def update_meal_log(request,pk):
    meal_log = get_object_or_404(MealLog, pk=pk)
    if request.method == 'POST':
        form = MealLogForm(request.POST, instance=meal_log)
        if form.is_valid():
            form.save()
            return redirect('meal-logs')
    else:
        form = MealLogForm(instance=meal_log)
    return render(request, 'meal_log_list.html', {'form': form})
    