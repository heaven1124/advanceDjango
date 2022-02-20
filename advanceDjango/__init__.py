from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app
import pymysql

from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver

# 向项目模块中增加celery_app对象
__all__ = ('celery_app',)

pymysql.install_as_MySQLdb()


def model_delete_pre(sender, **kwargs):
    from user.models import Order
    # sender表示哪个model的对象将要被删除，信号的发送者
    # kwargs表示信号的内容，信号传递的信息
    # print(sender)
    # print(kwargs) # key: signal,instance,using--数据保存位置
    info = 'Prepare Delete %s 类的 num=%s, title=%s'
    if sender == Order:
        print(info % (sender.__class__.__name__,
              kwargs.get('instance').num,
              kwargs.get('instance').title))


@receiver(post_delete)
def delete_model_post(sender, **kwargs):
    print(sender, 'delete success', kwargs)


pre_delete.connect(model_delete_pre)