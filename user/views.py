import json
import random
import uuid
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from common import code
from common.code import new_code_str

# Create your views here.


# @csrf_exempt
# def regist(request, user_id=None):
#     lovers = ['h5', 'Java', 'Python', 'Linux', 'Oracle']
#     # 获取页面提交的多选列表选中的值
#     select_loves = request.GET.getlist('love')
#     return render(request, 'regist2.html', locals())

# @csrf_exempt
# def regist(request, user_id=None):
#     # request.META
#     # print(request.body)
#
#     # print(request.method)
#     # print(request.POST)
#     # 返回对象类型是MultiValueDict，
#     # 文件对象类型是InMemoryUploadedFile
#     # print(request.FILES)
#
#     name = request.POST.get('name')
#     phone = request.POST.get('phone')
#     upload_file: InMemoryUploadedFile = request.FILES.get('img1')
#     if upload_file:
#         # print(upload_file.name)
#         # 文件类型，MIMETYPE image/png
#         # print(upload_file.content_type)
#         # print(upload_file.size)
#         # print(upload_file.charset)
#
#         # 上传文件必须是图片且小于50k
#         if all((
#             upload_file.content_type.startswith('image/'),
#             upload_file.size <= 50*1024
#         )):
#             print(request.META.get('REMOTE_ADDR'), '上传了', upload_file.name)
#             filename = name + os.path.splitext(upload_file.name)[-1]
#
#             with open('images/' + filename, 'wb') as f:
#                 # 分段写入
#                 for chunk in upload_file.chunks():
#                     f.write(chunk)
#                 f.flush()
#             return HttpResponse('upload success!')
#         else:
#             return HttpResponse('请上传小于50k的图片')
#
#     return render(request, 'regist4.html', locals())
from user.models import Order


@csrf_exempt
def regist(request):
    resp1 = HttpResponse(content='hello'.encode('utf-8'),
                         status=200,
                         content_type='text/html;charset=utf-8')
    with open('images/m.jpg', 'rb') as f:
        b = f.read()
    # 向客户端响应图片数据
    resp2 = HttpResponse(content=b, content_type='image/jpeg')
    # 设置响应头
    resp2.setdefault('Content-Length', len(b))
    # resp2.setdefault('Content-Type', 'image/jpg')

    # 响应json数据
    data = {'name': 'alan', 'age': 20}
    resp3 = HttpResponse(content=json.dumps(data), # 序列化字典对象，把字典对象转成字符串
                         content_type='application/json')
    resp4 = JsonResponse(data)
    return resp4


def add_cookie(request):
    # 生成token并存储到cookie中
    token = uuid.uuid4().hex
    resp = HttpResponse('增加cookie：token成功！')
    from datetime import datetime, timedelta
    resp.set_cookie('token', token,
                    expires=datetime.now()+timedelta(days=3))
    return resp


def del_cookie(request):
    resp = HttpResponse('删除cookie：token成功！')
    resp.delete_cookie('token')
    # 删除所有cookie
    # request.session.clear()
    for k in request.COOKIES:
        resp.delete_cookie(k)
    return resp


def login(request):
    phone = request.GET.get('phone')
    code = request.GET.get('code')
    # if all((
    #     phone == request.session.get('phone'),
    #     code == request.session.get('code')
    # )):
    if all((cache.has_key(phone),
            cache.get(phone) == code)):
        resp = HttpResponse('login success')
        resp.set_cookie('token', uuid.uuid4().hex)
        # 登陆成功，删除缓存
        cache.delete(phone)
        return resp

    return HttpResponse('fail login')


def logout(request):
    request.session.clear()
    #request.session.flush()
    resp = HttpResponse('注销成功')
    resp.delete_cookie('token')
    return resp


def list(request):
    # 验证是否登陆
    return HttpResponse('请先登陆')


def new_code(request):
    # 生成手机验证码 随机产生：大小写字母+数字
    code_txt = code.new_code_str(4)
    print(code_txt)
    phone = request.GET.get('phone')
    # 保存到session中 向手机发送验证码
    request.session['code'] = code_txt
    request.session['phone'] = phone
    # 将验证码存到cache中
    cache.set(phone, code_txt, timeout=60)
    return HttpResponse('成功发送验证码')


def new_img_code(request):
    # 创建画布
    img = Image.new('RGB', (150, 50), (100, 100, 0))
    # 获取画笔，绑定到画布
    draw = ImageDraw.Draw(img, 'RGB')
    # 创建字体颜色和字体对象
    font_color = (0, 20, 100)
    font = ImageFont.truetype(font='static/fonts/bw.ttf',
                              size=30)

    verification_code = new_code_str(6)
    request.session['code'] = verification_code

    draw.text((5, 5), verification_code, font=font, fill=font_color)
    draw.line((0, 0), (255, 0, 0), 20)
    for _ in range(500):
        x = random.randint(0, 150)
        y = random.randint(0, 50)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        draw.point((x, y), (r, g, b))
    # 将画布写入内存字节数组中
    buffer = BytesIO()
    img.save(buffer, 'png')

    return HttpResponse(content=buffer.getvalue(),
                        content_type='image/png')


def order_list(request):
    wd = request.GET.get('wd', '')
    page = request.GET.get('page', 1)
    orders = Order.objects.filter(Q(title__icontains=wd)).all() # 忽略大小写
    # 分页器
    paginator = Paginator(orders, 5)
    # 查询第page页
    pager = paginator.page(page)
    return render(request, 'list.html', locals())