from django.db import models


class Employee(models.Model):
    empl_id = models.IntegerField()
    fio = models.CharField(max_length=255)
    post = models.CharField(max_length=50)
    date_create = models.DateField()
    salary = models.IntegerField()
    # boss = models.IntegerField()
    boss = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.fio
