from django.db import models


""" PLANTS > DISEASES > CANOPIES """


class Predication(models.Model):
    GENDER_CHOICES = (
        (1, 'Male'),
        (0, 'Female'),
    )
    CHEST_PAIN_TYPE_CHOICES = (
        (1, 'Typical'),
        (2, 'Typical Angina'),
        (3, 'Non Anginal Pain'),
        (4, 'Asymptomatic'),
    )
    RESTING_ECG_CHOICES = (
        (0, 'Normal'),
        (1, 'Abnormality in ST-T Wave'),
        (2, 'Left Ventricular Hypertrophy'),
    )
    EXERCISE_ANGINA_CHOICES = (
        (0, 'Depicting No'),
        (1, 'Depicting Yes'),
    )
    ST_SLOPE_CHOICES = (
        (0, 'Normal'),
        (1, 'Up Sloping'),
        (2, 'Flat'),
        (3, 'Down Sloping'),
    )
    TARGET_CHOICES = (
        (0, 'Normal'),
        (1, 'Patient is suffering from heart risk'),
    )

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    age = models.PositiveIntegerField()
    gender = models.PositiveIntegerField(choices=GENDER_CHOICES)

    resting_bp_s = models.PositiveIntegerField()
    cholestrol = models.PositiveIntegerField()
    fasting_blood_sugar = models.PositiveIntegerField()
    old_peak = models.PositiveIntegerField()

    chest_pain_type = models.PositiveIntegerField(choices=CHEST_PAIN_TYPE_CHOICES)
    target = models.PositiveIntegerField(choices=TARGET_CHOICES)
    st_slope = models.PositiveIntegerField(choices=ST_SLOPE_CHOICES)
    exercise_angina = models.PositiveIntegerField(choices=EXERCISE_ANGINA_CHOICES)

    resting_ecg = models.PositiveIntegerField(choices=RESTING_ECG_CHOICES)
    max_heart_rate = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
