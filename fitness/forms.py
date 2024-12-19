from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser,WorkoutLog,MealLog
import json

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'age', 'weight', 'height', 'goal', 'activity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['goal'].widget.attrs.update({'class': 'form-select'})
        self.fields['activity'].widget.attrs.update({'class': 'form-select'})


class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['workout', 'exercises_completed', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add notes about your workout...'}),
        }

    def clean_exercises_completed(self):
        exercises_completed = self.cleaned_data['exercises_completed']

        try:
            completed_exercises = json.loads(exercises_completed)
        except json.JSONDecodeError:
            raise forms.ValidationError("Exercises completed must be a valid JSON array.")

        if self.instance.workout:
            workout_exercises = json.loads(self.instance.workout.exercises)
            workout_exercise_names = [exercise['name'] for exercise in workout_exercises]
            for exercise in completed_exercises:
                if exercise not in workout_exercise_names:
                    raise forms.ValidationError(f"Exercise '{exercise}' is not part of the selected workout.")

        return exercises_completed

class MealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['meal_type', 'notes']
