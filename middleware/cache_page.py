from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache


class CachePageMiddleware(MiddlewareMixin):
    # 配置需要缓存的页面路径
    cache_page_path = [
        '/user/list/'
    ]

    def process_request(self, request):
        # 判断当前请求的页面是否支持缓存
        if request.path in self.cache_page_path:
            # 判断页面是否已缓存
            # if cache.has_key(request.path): 过时方法
            if request.path in cache:
                return HttpResponse(cache.get(request.path))

    def process_response(self, request, response):
        # 判断当前请求的页面是否支持缓存
        if request.path in self.cache_page_path:
            # 把页面放入缓存中
            cache.set(request.path, response.content, timeout=60)
        return response
