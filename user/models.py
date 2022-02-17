from django.db import models

# Create your models here.


class Order(models.Model):
    __pay_status_tuple__ = ((0, '待支付'),
                            (1, '已支付'),
                            (2, '待收货'),
                            (3, '已收货'),
                            (4, '已完成'),
                            (5, '已取消'))

    num = models.CharField(max_length=20,
                           primary_key=True,
                           verbose_name='订单号')
    title = models.CharField(max_length=100,
                             verbose_name='订单标题')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='订单金额')
    pay_type = models.IntegerField(choices=((0, '余额'),
                                            (1, '银行卡'),
                                            (2, '微信'),
                                            (3, '支付宝')),
                                   verbose_name='支付方式',
                                   default=0)
    pay_status = models.IntegerField(choices=__pay_status_tuple__,
                                     verbose_name='订单状态',
                                     default=0)
    receiver = models.CharField(verbose_name='收货人',
                                max_length=20)
    receiver_phone = models.CharField(verbose_name='收货人电话',
                                      max_length=11)
    receiver_address = models.TextField(verbose_name='收货地址')

    @property
    def pay_status_title(self):
        return self.__pay_status_tuple__[self.pay_status][1]

    def __str__(self):
        return self.title

    class Meta:
        db_table = 't_order'
        verbose_name = verbose_name_plural = '订单表'
