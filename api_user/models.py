from django.db import models

# Create your models here.
class UserModel(models.Model):
    user_id = models.CharField(primary_key=True, max_length=12)
    user_pw = models.CharField(max_length=255, null=False)
    user_nm = models.CharField(max_length=20, null=False, default='')
    user_mobile_no = models.CharField(max_length=20, null=False, default='')
    user_ty = models.CharField(max_length=1, null=False, default='0')
    device_token = models.CharField(max_length=255, null=False, default='')
    cre_dt = models.DateTimeField(auto_now_add=True)
    cre_id = models.CharField(max_length=20, blank=True, null=True)
    upt_dt = models.DateTimeField(auto_now=True)
    upt_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        ordering = ('user_nm',)
        db_table = 'tb_user_info'


class TbCommuteInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    attendee_time = models.CharField(blank=True, null=True, max_length=20)
    quitting_time = models.CharField(blank=True, null=True, max_length=20)  # Field renamed to remove unsuitable characters.
    user_id = models.CharField(max_length=30)
    register_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        ordering = ('id',)
        db_table = 'tb_commute_info'
