from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(MealPlans)
admin.site.register(Workout)
admin.site.register(WorkoutLog)
admin.site.register(UserDashboardMetric)
admin.site.register(ActivityLevel)
admin.site.register(MealLog)

