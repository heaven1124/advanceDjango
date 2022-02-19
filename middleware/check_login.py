import logging

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CheckLoginMiddleware(MiddlewareMixin):

    # 从请求到来到路由urls过程，触发此函数
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = request.get_host()
        msg = '%s 访问 %s' % (ip, path)
        # 打印日志
        logging.getLogger('django').info(msg)

        # print('------CheckLoginMiddleware-----', 'process_request')
        print(request.path, request.COOKIES)

        # 设置中间件不拦截下面路由
        notfilters = ['/user/login/', '/user/code/']
        if request.path not in notfilters:
            # 验证用户是否登陆
            if not request.COOKIES.get('token'):
                return HttpResponse('<h3>Login</h3><form><input><button>Login</button></form>')

    # def process_view(self, request, callback, callback_args, callback_kwargs):
    #     print('------CheckLoginMiddleware-----', 'process_view')
    #     # callback是views.py里面的函数或view的实现类，callback_args, callback_kwargs是函数的参数
    #     # 新增一个关键参数page，类似于在匹配路由中添加一个参数page，stock/<stock_id>/<page>/
    #     callback_kwargs['page'] = request.GET.get('page', 1)
    #     print(callback, callback_args, callback_kwargs)

    # def process_response(self, request, response):
    #     print('------CheckLoginMiddleware-----', 'process_response')
    #     return response # 必须返回response响应对象

    def process_exception(self, request, exception):
        print('------CheckLoginMiddleware-----', 'process_exception')
        print(exception, type(exception))
        return HttpResponse('业务处理过程中出现异常：%s' % exception)
