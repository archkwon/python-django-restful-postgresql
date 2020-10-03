from django.db import models

# Create your models here.
class DeliveryMasterModel(models.Model):
    DELIVERY_STATE_CODE = (
        ('A', '배송출발'),
        ('C', '배송완료')
    )

    master_seq = models.CharField(primary_key=True, max_length=20, verbose_name='배송코드')
    memo_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='메모코드')
    order_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='주문코드')
    cust_code = models.CharField(max_length=6, blank=True,  null=True, verbose_name='거래처코드')
    cust_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='거래처명')
    cust_lat = models.CharField(max_length=30, blank=True, null=True, verbose_name='거래처위도')
    cust_lng = models.CharField(max_length=30, blank=True, null=True, verbose_name='거래처경도')
    cust_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='거래처주소')
    distance = models.FloatField(max_length=20, blank=True, null=True, verbose_name='거래처거리')
    delivery_date = models.CharField(max_length=20, blank=True, null=True, verbose_name='배송시작일자')
    driver_mobile_num = models.CharField(max_length=20, blank=True, null=True, verbose_name='기사휴대폰')
    driver_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='기사명')
    delivery_state_code = models.CharField(max_length=1, blank=True, null=True, verbose_name='배송상태', choices=DELIVERY_STATE_CODE)
    delivery_message = models.TextField(null=True, blank=True, verbose_name='메모')
    part_count = models.CharField(max_length=3, null=True, blank=True, verbose_name='상품개수')
    save_date = models.DateTimeField(auto_now_add=True, verbose_name='저장일자')
    complete_date = models.CharField(max_length=20, blank=True, null=True, verbose_name='배송완료일자')
    image_file_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='배송이미지')

    class Meta:
        managed = False
        ordering = ['master_seq']
        db_table = 'tb_delivery_master'
        verbose_name = "배송관리"
        verbose_name_plural = "배송관리"


class DeliveryPartModel(models.Model):
    part_seq = models.CharField(primary_key=True, max_length=30)
    master_seq = models.CharField(max_length=20)
    part_code = models.CharField(max_length=6, blank=True, null=True)
    part_name = models.CharField(max_length=100, blank=True, null=True)
    save_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        ordering = ['part_seq']
        db_table = 'tb_delivery_part'


class DeliveryFileModel(models.Model):
    file_seq = models.CharField(primary_key=True, max_length=100)
    master_seq = models.CharField(max_length=30, blank=True, null=True)
    image_file = models.FileField()
    image_file_url = models.CharField(max_length=500, blank=True, null=True)
    save_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        ordering = ['file_seq']
        db_table = 'tb_delivery_file_info'