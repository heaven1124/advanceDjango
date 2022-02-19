from datetime import datetime
from django.views.generic import RedirectView
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View

# Create your views here.

# @csrf_exempt
# def goods(request):
#     # 分发请求
#     method = request.method
#     handler = goods_get if method == 'GET' else goods_post
#     return handler(request)
#
#
# def goods_get(request):
#     return render(request, 'stock/list.html', locals())
#
#
# def goods_post(request):
#     return HttpResponse('post request')


class StockView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        stock_id = kwargs.get('stock_id')
        page = kwargs.get('page', 5)
        return render(request, 'stock/list.html', locals())

    def post(self, request):
        return HttpResponse('post request')

    def put(self, request):
        return HttpResponse('put request')

    def delete(self, request):
        return HttpResponse('delete request')


class GoodsView(TemplateView):

    # 渲染模板之前，提供扩展上下文数据
    extra_context = {'msg': 'I am extra msg'}
    template_name = 'goods/list.html'

    # 渲染模板之前，提供上下文数据，只针对get请求
    def get_context_data(self, **kwargs):
        context = super(GoodsView, self).get_context_data(**kwargs)
        wd = context.get('wd', '')

        datas = ['iphone6', 'iphone7', 'iphone8'] if wd == 'iphone'\
            else ['vivo', 'huawei']

        context['datas'] = datas
        context['msg'] = '查询成功 %s' % (datetime.now())
        return context


class QueryView(RedirectView):

    pattern_name = 'stockapp:goods'

    # 重定向之前，自动拼接查询参数
    query_string = True

    # url = ''
    # query_string = False
    # permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return super(QueryView, self).get_redirect_url(*args, **kwargs)