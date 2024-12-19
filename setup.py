import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_tracker.settings')
django.setup()

from fitness.models import ActivityLevel, Workout

def populate_database():
    # Populate Activity Levels
    activity_levels = [
        {
            "level": "Sedentary",
            "description": "Little or no exercise",
            "multiplier": 1.2
        },
        {
            "level": "Lightly Active",
            "description": "Light exercise 1-3 days/week",
            "multiplier": 1.375
        },
        {
            "level": "Moderately Active",
            "description": "Moderate exercise 3-5 days/week",
            "multiplier": 1.55
        },
        {
            "level": "Very Active",
            "description": "Hard exercise 6-7 days/week",
            "multiplier": 1.725
        },
        {
            "level": "Extra Active",
            "description": "Very hard exercise & physical job",
            "multiplier": 1.9
        }
    ]

    for activity in activity_levels:
        obj, created = ActivityLevel.objects.get_or_create(**activity)
        if created:
            print(f"Added activity level: {obj.level}")
        else:
            print(f"Activity level already exists: {obj.level}")

    # Populate Workouts
    workouts = [
        {
            "name": "Full Body Strength",
            "description": "A beginner's full-body strength workout to build muscle mass. Focuses on basic compound movements.",
            "exercises": '[{"name": "Push-ups", "met": 8, "duration_minutes": 7.5}, {"name": "Bodyweight squats", "met": 5.5, "duration_minutes": 7.5}, {"name": "Dumbbell rows", "met": 6, "duration_minutes": 7.5}, {"name": "Plank hold (30 seconds)", "met": 3, "duration_minutes": 7.5}]',
            "difficulty": "Beginner",
            "duration_minutes": 30,
            "target_goal": "Weight Gain",
        },
        {
            "name": "Mass Building Workout",
            "description": "A more intense workout with weighted exercises to increase strength and muscle size.",
            "exercises": '[{"name": "Barbell squats", "met": 6, "duration_minutes": 8}, {"name": "Dumbbell bench press", "met": 5, "duration_minutes": 8}, {"name": "Pull-ups", "met": 8, "duration_minutes": 8}, {"name": "Deadlifts", "met": 6, "duration_minutes": 8}, {"name": "Shoulder press", "met": 5, "duration_minutes": 8}]',
            "difficulty": "Intermediate",
            "duration_minutes": 40,
            "target_goal": "Weight Gain",
        },
        {
            "name": "Powerlifting Strength Routine",
            "description": "A strength-focused workout using heavy weights and progressive overload.",
            "exercises": '[{"name": "Barbell back squats", "met": 6, "duration_minutes": 10}, {"name": "Barbell deadlifts", "met": 6, "duration_minutes": 10}, {"name": "Barbell bench press", "met": 5, "duration_minutes": 10}, {"name": "Weighted lunges", "met": 6.5, "duration_minutes": 10}, {"name": "Barbell rows", "met": 6, "duration_minutes": 10}]',
            "difficulty": "Advanced",
            "duration_minutes": 50,
            "target_goal": "Weight Gain",
        },
        {
            "name": "Full Body Fat Burn",
            "description": "A beginner cardio and bodyweight workout designed to burn fat and improve stamina.",
            "exercises": '[{"name": "Jumping jacks", "met": 8, "duration_minutes": 6}, {"name": "High knees", "met": 8, "duration_minutes": 6}, {"name": "Bodyweight squats", "met": 5.5, "duration_minutes": 6}, {"name": "Push-ups", "met": 8, "duration_minutes": 6}, {"name": "Burpees (low intensity)", "met": 6, "duration_minutes": 6}]',
            "difficulty": "Beginner",
            "duration_minutes": 30,
            "target_goal": "Weight Loss",
        },
        {
            "name": "Intermediate HIIT Workout",
            "description": "High-Intensity Interval Training workout to torch fat and improve endurance.",
            "exercises": '[{"name": "Burpees", "met": 10, "duration_minutes": 6}, {"name": "Mountain climbers", "met": 8, "duration_minutes": 6}, {"name": "Jump squats", "met": 8.5, "duration_minutes": 6}, {"name": "High knees", "met": 8, "duration_minutes": 6}, {"name": "Plank to push-up", "met": 5, "duration_minutes": 6}]',
            "difficulty": "Intermediate",
            "duration_minutes": 30,
            "target_goal": "Weight Loss",
        },
        {
            "name": "High-Intensity Circuit Training",
            "description": "A circuit-based workout combining cardio and strength exercises to maximize fat burn.",
            "exercises": '[{"name": "Sprint intervals", "met": 12, "duration_minutes": 8}, {"name": "Jumping lunges", "met": 8.5, "duration_minutes": 8}, {"name": "Push-ups", "met": 8, "duration_minutes": 8}, {"name": "Russian twists", "met": 4, "duration_minutes": 8}, {"name": "Bicycle crunches", "met": 6, "duration_minutes": 8}]',
            "difficulty": "Advanced",
            "duration_minutes": 40,
            "target_goal": "Weight Loss",
        },
        {
            "name": "Full Body Beginner Maintenance Routine",
            "description": "A beginner workout that combines strength and cardio for weight maintenance and overall fitness.",
            "exercises": '[{"name": "Bodyweight squats", "met": 5.5, "duration_minutes": 6}, {"name": "Push-ups", "met": 8, "duration_minutes": 6}, {"name": "Jumping jacks", "met": 8, "duration_minutes": 6}, {"name": "Plank hold", "met": 3, "duration_minutes": 6}, {"name": "Walking lunges", "met": 5, "duration_minutes": 6}]',
            "difficulty": "Beginner",
            "duration_minutes": 30,
            "target_goal": "Weight Maintenance",
        },
        {
            "name": "Strength & Cardio Fusion",
            "description": "A balanced workout combining strength training and cardio exercises to maintain weight and build strength.",
            "exercises": '[{"name": "Dumbbell lunges", "met": 6.5, "duration_minutes": 8}, {"name": "Barbell squats", "met": 6, "duration_minutes": 8}, {"name": "Jump rope", "met": 12, "duration_minutes": 8}, {"name": "Push-ups", "met": 8, "duration_minutes": 8}, {"name": "Kettlebell swings", "met": 8, "duration_minutes": 8}]',
            "difficulty": "Intermediate",
            "duration_minutes": 40,
            "target_goal": "Weight Maintenance",
        },
        {
            "name": "Advanced Endurance + Strength Routine",
            "description": "A challenging full-body routine combining heavy lifting and high-intensity cardio to maintain weight and push endurance limits.",
            "exercises": '[{"name": "Deadlifts", "met": 6, "duration_minutes": 9}, {"name": "Barbell squats", "met": 6, "duration_minutes": 9}, {"name": "Box jumps", "met": 10, "duration_minutes": 9}, {"name": "Battle ropes", "met": 12, "duration_minutes": 9}, {"name": "Pull-ups", "met": 8, "duration_minutes": 9}]',
            "difficulty": "Advanced",
            "duration_minutes": 45,
            "target_goal": "Weight Maintenance",
        },
    ]

    for workout in workouts:
        obj, created = Workout.objects.get_or_create(**workout)
        if created:
            print(f"Added workout: {obj.name}")
        else:
            print(f"Workout already exists: {obj.name}")

    print("Database populated successfully!")

if __name__ == '__main__':
    populate_database()
