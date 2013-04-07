from django.db import models

class People(models.Model):
    GENDER_CHOICES = (
        ('MAL', 'Male'),
        ('FEM', 'Female')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    gender = models.CharField(max_length=3,
                              choices=GENDER_CHOICES)
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
