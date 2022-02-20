from celery import shared_task


@shared_task
def qbuy(goods_id, user_id):
    print('goods_id: %s -> user_id: %s'% (goods_id, user_id))
    return '%s ok %s' % (goods_id, user_id)