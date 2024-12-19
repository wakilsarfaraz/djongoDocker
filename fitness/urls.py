from django.urls import path
from .views import signup,user_login,user_logout,DashboardView,password_change,WorkoutLogListView,MealLogListView,workout_exercises,add_workout_log,update_workout_log,WorkoutLogDeleteView,MealLogDeleteView,meal_log_create,update_meal_log

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path("change-password/", password_change, name='change-password'),
    path('workout-logs/',WorkoutLogListView.as_view(),name='workout-logs'),
    path('meal-logs/',MealLogListView.as_view(),name='meal-logs'),
    path('workout-logs/add/', add_workout_log, name='workout-log-create'),
    path('workout-exercises/<int:workout_id>/', workout_exercises, name='workout-exercises'),
    path('workout-logs/<int:pk>/update/', update_workout_log, name='workout-log-update'),
    path('workout-logs/<int:pk>/delete/', WorkoutLogDeleteView.as_view(), name='workout-log-delete'),
    path('meal-logs/<int:pk>/delete/', MealLogDeleteView.as_view(), name='meal-log-delete'),
    path('meal-logs/add/', meal_log_create, name='meal-log-create'),
    path('meal-logs/<int:pk>/update/', update_meal_log, name='meal-log-update'),
]