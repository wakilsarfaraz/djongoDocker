from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from django.utils.timezone import now

User = get_user_model()


class ActivityLevel(models.Model):
    level = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    multiplier = models.FloatField()
    def __str__(self):
        return self.level


Goals = (('Weight gain','Weight gain'),('Lose weight','Lose weight'),('Maintain','Maintain'))
class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='auth_user')  
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    goal = models.CharField(max_length=100,choices=Goals)
    activity = models.ForeignKey(ActivityLevel, on_delete=models.SET_NULL, null=True, blank=True, db_column='activity')
    daily_caloric_intake = models.IntegerField(blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)
    bmi_status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Calculate BMI
        if self.height > 0:
            self.bmi = self.weight / (self.height / 100) ** 2
            # Determine BMI status
            if self.bmi < 18.5:
                self.bmi_status = 'Underweight'
            elif 18.5 <= self.bmi < 24.9:
                self.bmi_status = 'Normal'
            elif 25 <= self.bmi < 29.9:
                self.bmi_status = 'Overweight'
            else:
                self.bmi_status = 'Obese'

        # Calculate daily caloric intake for maintenance
        if self.activity:
            caloric_intake = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5  # Mifflin-St Jeor formula for males
            caloric_intake *= self.activity.multiplier  

            # Set daily caloric intake to maintain weight
            self.daily_caloric_intake = int(caloric_intake)

        super().save(*args, **kwargs)
        self.generate_meal_plan()
    def generate_meal_plan(self):
            # Determine the caloric goal based on user's goal
            if self.goal == "Lose weight":
                calories_goal = int(self.daily_caloric_intake * 0.8)  # 20% deficit
            elif self.goal == "Weight gain":
                calories_goal = int(self.daily_caloric_intake * 1.1)  # 10% surplus
            else:
                calories_goal = self.daily_caloric_intake  # Maintain weight

            # Auto-generate meal plan based on the calories goal
            meal_plan_data = {
                'calories_goal': calories_goal,
                'meals': json.dumps([
                    {"name": "Breakfast", "calories": calories_goal * 0.25, "protein": 25, "carbs": 30, "fats": 10},
                    {"name": "Lunch", "calories": calories_goal * 0.35, "protein": 30, "carbs": 50, "fats": 15},
                    {"name": "Dinner", "calories": calories_goal * 0.3, "protein": 25, "carbs": 40, "fats": 12},
                    {"name": "Snack", "calories": calories_goal * 0.1, "protein": 10, "carbs": 15, "fats": 5}
                ])
            }

            # Check if the user already has a meal plan for today
            today = now().date()
            meal_plan, created = MealPlans.objects.update_or_create(
                user=self,
                date=today,
                defaults=meal_plan_data
            )

class MealPlans(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    calories_goal = models.IntegerField()
    calories_consumed = models.IntegerField(editable=False)
    meals = models.TextField()  
    def __str__(self) :
        return f'{self.user} meals'
    def save(self, *args, **kwargs):
        # Calculate total calories from meals
        try:
            meals_data = json.loads(self.meals)  
            self.calories_consumed = sum(meal.get("calories", 0) for meal in meals_data)
        except (json.JSONDecodeError, TypeError):
            self.calories_consumed = 0  
        
        super().save(*args, **kwargs)


class Workout(models.Model):
    GOAL_CHOICES = [
        ('Weight Gain', 'Weight Gain'),
        ('Weight Loss', 'Weight Loss'),
        ('Weight Maintenance', 'Weight Maintenance'),
    ]

    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    exercises = models.TextField()  
    difficulty = models.CharField(max_length=50,choices=DIFFICULTY_CHOICES)
    duration_minutes = models.PositiveIntegerField()
    target_goal = models.CharField(max_length=50,choices=GOAL_CHOICES,null=True,blank=True)
    def __str__(self):
        return f'{self.name} - {self.difficulty}'



class WorkoutLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    workout = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    exercises_completed = models.TextField()  
    total_calories_burned = models.PositiveIntegerField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    '''
    to auto calc an estimate of calories burned based on the formula:
    Calories Burned=MET×Weight in kg×Duration in hours
    '''
    def save(self, *args, **kwargs):
        if self.workout:
            exercises_completed = json.loads(self.exercises_completed)
            
            total_calories_burned = 0
            total_duration = 0
            
            workout_exercises = json.loads(self.workout.exercises)
            
            for exercise_name in exercises_completed:
                for exercise in workout_exercises:
                    if isinstance(exercise, dict):
                        if exercise['name'] == exercise_name:
                            total_calories_burned += (self.user.weight * (exercise['duration_minutes'] / 60) * exercise['met'])
                            total_duration += exercise['duration_minutes']
            
            self.total_calories_burned = total_calories_burned
            self.duration_minutes = total_duration
            
        super().save(*args, **kwargs)



class UserDashboardMetric(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise_sessions = models.PositiveIntegerField(blank=True, null=True)
    total_calories_consumed = models.PositiveIntegerField(blank=True, null=True)
    total_calories_burned = models.PositiveIntegerField(blank=True, null=True)
    average_daily_calories = models.PositiveIntegerField(blank=True, null=True)
    average_daily_exercises = models.PositiveIntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.name} - Dashboard Metrics"

class MealLog(models.Model):
    mealType = (('Breakfast','Breakfast'),('Lunch','Lunch'),('Dinner','Dinner'),('Snack','Snack'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    meal_plan = models.ForeignKey(MealPlans, on_delete=models.SET_NULL, null=True, blank=True)
    meal_type = models.CharField(max_length=50, blank=True, null=True,choices=mealType)
    calories_consumed = models.FloatField(blank=True, null=True)  
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.name} - {self.meal_type} on {self.date}"

    def save(self, *args, **kwargs):
        if self.meal_plan and self.meal_type:
            try:
                meals_data = json.loads(self.meal_plan.meals)

                meal_data = next(
                    (meal for meal in meals_data if meal['name'].lower() == self.meal_type.lower()),
                    None
                )

                if meal_data:
                    self.calories_consumed = meal_data['calories']

            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error parsing meals JSON: {e}")
                self.calories_consumed = None
        super().save(*args, **kwargs)



@receiver(post_save, sender=WorkoutLog)
@receiver(post_save, sender=MealLog)
def create_or_update_user_dashboard_metrics(sender, instance, **kwargs):
    if instance.user:
        metrics, created = UserDashboardMetric.objects.get_or_create(user=instance.user)
        
        # Calculate total calories consumed from MealLogs using `calories_consumed`
        total_calories_consumed = MealLog.objects.filter(user=instance.user).aggregate(
            total_calories=models.Sum('calories_consumed')  
        )['total_calories'] or 0

        distinct_dates = MealLog.objects.filter(user=instance.user).values_list('date', flat=True).distinct()
        days_logged = len(distinct_dates)

        average_daily_calories = (
            total_calories_consumed // days_logged if days_logged > 0 else 0
        )
        exercise_sessions = WorkoutLog.objects.filter(user=instance.user).count()

        total_calories_burned = WorkoutLog.objects.filter(user=instance.user).aggregate(
            total_calories=models.Sum('total_calories_burned')
        )['total_calories'] or 0

        distinct_exercise_dates = WorkoutLog.objects.filter(user=instance.user).values_list('date', flat=True).distinct()
        days_logged_exercises = len(distinct_exercise_dates)

        average_daily_exercises = (
            exercise_sessions // days_logged_exercises if days_logged_exercises > 0 else 0
        )

        # Update the metrics
        metrics.total_calories_consumed = total_calories_consumed
        metrics.average_daily_calories = average_daily_calories
        metrics.exercise_sessions = exercise_sessions
        metrics.total_calories_burned = total_calories_burned
        metrics.average_daily_exercises = average_daily_exercises
        metrics.last_updated = now() 
        metrics.save()
