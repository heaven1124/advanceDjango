from signals import codeSignal
from django.dispatch import receiver


# 接收信号
@receiver(codeSignal)
def cache_code(sender, **kwargs):
    print(sender, kwargs)