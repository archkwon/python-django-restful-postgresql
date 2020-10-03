from django.db import models

# Create your models here.
class LocationModel(models.Model):
    seq = models.CharField(max_length=20, primary_key=True)
    user_id = models.CharField(max_length=12, null=False)
    user_nm = models.CharField(max_length=20, null=False)
    user_mobile_no = models.CharField(max_length=20, null=False)
    lat = models.CharField(max_length=30, null=False)
    lng = models.CharField(max_length=30, null=False)
    save_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        ordering = ['-seq']
        db_table = 'tb_location_info'