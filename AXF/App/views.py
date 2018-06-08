from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from .models import *
import os
from AXF.settings import MEDIA_ROOT
import uuid
import hashlib


# 首页
def home(request):
    # 轮播数据
    wheels = MainWheel.objects.all()

    # 导航数据
    navs = MainNav.objects.all()

    # 必购数据
    mustbuys = MainMustbuy.objects.all()

    # shop数据
    shops = MainShop.objects.all()
    shop0 = shops.first()
    shop1_2 = shops[1:3]
    shop3_6 = shops[3:7]
    shop7_10 = shops[7:11]

    # 主要商品数据
    mainshows = MainShow.objects.all()

    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shop0': shop0,
        'shop1_2': shop1_2,
        'shop3_6': shop3_6,
        'shop7_10': shop7_10,
        'mainshows': mainshows,

    }
    return render(request, 'home/home.html', data)


# 闪购
def market(request):
    return redirect(reverse('App:market_with_params', args=['104749', '0', '0']))


# 带参数的闪购
def market_with_params(request, typeid, typechildid, sortid):
    # 分类数据
    foodtypes = FoodType.objects.all()

    # 商品数据,根据主分类id进行筛选
    goods_list = Goods.objects.filter(categoryid=typeid)

    # 再按照子分类进行筛选
    if typechildid != '0':
        goods_list = goods_list.filter(childcid=typechildid)

    # 获取当前主分类下的所有子分类
    childnames = FoodType.objects.filter(typeid=typeid)

    child_type_list = []
    if childnames.exists():
        childtypes = childnames.first().childtypenames.split('#')

        for type in childtypes:
            type_list = type.split(':')
            child_type_list.append(type_list)

    # 排序规则
    if sortid == '0':  # 综合排序
        pass
    elif sortid == '1':  # 销量排序
        goods_list = goods_list.order_by('-productnum')
    elif sortid == '2':  # 价格降序
        goods_list = goods_list.order_by('-price')
    elif sortid == '3':  # 价格升序
        goods_list = goods_list.order_by('price')

    data = {
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'typeid': typeid,
        'child_type_list': child_type_list,
        'typechildid': typechildid,

    }

    return render(request, 'market/market.html', data)


# 我的
def mine(request):
    data = {
        'name': '',
        'icon': '',

    }

    # 获取session
    userid = request.session.get('userid', '')

    if userid:
        user = User.objects.get(id=userid)
        name = user.name  # 用户名
        icon = user.icon  # 头像名称
        data['name'] = name
        data['icon'] = '/upload/icon/' + icon

    return render(request, 'mine/mine.html', data)


# 注册
def register(request):
    return render(request, 'user/register.html')


# 注册操作
def register_handle(request):
    data = {
        'status': 1,
        'msg': 'ok'
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon', "")

        # 检测提交过来的数据是否合法
        if len(username) < 6:
            data['status'] = 0
            data['msg'] = '用户名输入不合法'
            return render(request, 'user/register.html', data)

        # 注册
        try:
            user = User()
            user.name = username
            user.password = password
            user.email = email

            # 头像
            if icon:
                filename = random_file() + '.png'  # icon.name
                user.icon = filename

                filepath = os.path.join(MEDIA_ROOT, filename)
                with open(filepath, 'ab') as fp:
                    for part in icon.chunks():
                        fp.write(part)
                        fp.flush()

            else:
                user.icon = ""
            user.save()

            # 保存session
            request.session['userid'] = user.id

            return redirect(reverse('App:mine'))
        except:
            return redirect(reverse('App:register'))

    return redirect(reverse('App:register'))


# 获取随机的文件名称
def random_file():
    u = str(uuid.uuid4())
    m = hashlib.md5()
    m.update(u.encode('utf-8'))
    return m.hexdigest()


# 退出登录
def logout(request):
    # 删除session
    request.session.flush()
    return redirect(reverse('App:mine'))


# 用户名检测
def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username')

        # 检测用户名是否存在
        users = User.objects.filter(name=username)

        # 如果存在
        if users.exists():
            return JsonResponse({'status': 0, 'msg': '用户名已存在'})
        # 如果不存在
        else:
            return JsonResponse({'status': 1, 'msg': 'ok'})

    return JsonResponse({'status': -1, 'msg': '请求方式错误'})


# 登录
def login(request):
    return render(request, 'user/login.html')


# 登录操作
def login_handle(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 匹配用户名和密码
        users = User.objects.filter(name=username, password=password)
        if users.exists():
            # 如果登录成功，则进入我的页面
            # 保存session

            request.session['userid'] = users.first().id
            return redirect(reverse('App:mine'))
        else:
            data['status'] = 0
            data['msg'] = '用户名或密码错误'
            return render(request, 'user/login.html', data)

    data['status'] = -1
    data['msg'] = '请求方式不正确'
    return render(request, 'user/login.html', data)


# 购物车
def cart(request):
    # 检查是否登录
    userid = request.session.get('userid', '')
    if not userid:
        return redirect(reverse('App:login'))
    else:
        # 如果登录了，则获取当前登录用户的所以信息
        carts = Cart.objects.filter(user_id=userid)

        return render(request, 'cart/cart.html', {'carts': carts})


# 加入购物车
def add_to_cart(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    # 判断用户是否登录
    userid = request.session.get('userid', '')
    if not userid:
        data["status"] = 0
        data["msg"] = "请先登录"
    else:
        # 已登录
        if request.method == 'GET':
            goodsid = request.GET.get('goodsid')
            num = request.GET.get('num')

            # 先判断该商品是否已经在该用户的购物车中
            carts = Cart.objects.filter(goods_id=goodsid, user_id=userid)

            # 如果存在，则商品数量累加
            if carts.exists():
                cart = carts.first()
                cart.num += int(num)
                cart.save()

            else:
                # 添加到购物车
                cart = Cart()
                cart.user_id = userid
                cart.goods_id = goodsid
                cart.num = num
                cart.save()

        else:
            data["status"] = -1
            data["msg"] = "请求方式不正确"

    return JsonResponse(data)


# 数量+
def add_num(request):
    data = {
        'status': 1,
        'msg': 'ok',

    }

    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        # 如果登录了
        if request.method == 'GET':
            cartid = request.GET.get('cartid')

            # 数量+1
            cart = Cart.objects.get(id=cartid)
            cart.num += 1
            cart.save()
            data['num'] = cart.num

        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 数量-
def reduce_num(request):
    data = {
        'status': 1,
        'mag': 'ok'
    }
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        # 如果登录了
        if request.method == 'GET':
            cartid = request.GET.get('cartid')

            # 数量-1
            cart = Cart.objects.get(id=cartid)
            cart.num -= 1
            if cart.num < 1:
                cart.num = 1
            cart.save()
            data['num'] = cart.num

        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 删除
def delete_cart(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            cartid = request.GET.get('cartid')

            # 删除
            Cart.objects.filter(id=cartid).delete()
        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


# 勾选/取消勾选
def cart_select(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            cartid = request.GET.get('cartid')
            # 勾选/取消勾选

            cart = Cart.objects.get(id=cartid)
            cart.is_select = not cart.is_select
            cart.save()
            data['is_select'] = cart.is_select


        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


# 全选/取消全选
def cart_selectall(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            action = request.GET.get('action')
            selects = request.GET.get('selects')
            select_list = selects.split("#")  # [11,12,13,14,15]
            # print(action, selects)  # cancelselect 11#12#13#14#15

            #全不选
            if action == 'cancelselect':
                Cart.objects.filter(id__in=select_list).update(is_select=False)
            # 全选
            else:
                Cart.objects.filter(id__in=select_list).update(is_select=True)

        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


# 生成订单
def order_add(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':

            # 先获取当前用户的购物车中勾选的商品
            carts = Cart.objects.filter(user_id=userid, is_select=True)

            #生成订单
            order = Order()
            order.order_id = str(uuid.uuid4())
            order.user_id = userid
            order.save()

            #创建订单商品
            total = 0  # 总价
            for cart in carts:
                order_goods = OrderGoods()
                order_goods.goods_id = cart.goods_id
                order_goods.order_id = order.id
                order_goods.num =  cart.num
                order_goods.price = cart.goods.price
                order_goods.save()

                total += order_goods.num * order_goods.price

            # 添加总价
            order.order_price = total
            order.save()

            data['orderid'] = order.id

        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)

# 订单页面
def order (request, orderid):
    order = Order.objects.get(id=orderid)
    return render(request, 'order/order.html', {'order':order})


# 更改订单状态
def order_chang_status(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            orderid = request.GET.get('orderid')
            status = request.GET.get('status')

            #修改订单的状态为status
            Order.objects.filter(id=orderid).update(order_status=status)

        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)

# 待付款订单页面
def order_waitpay(request):
    userid = request.session.get('userid', '')
    if not userid:
        return redirect(reverse('App:login_handle'))
    else:
        # 如果登录了，则获取到当前用户下的所有待付款订单
        orders = Order.objects.filter(user_id = userid, order_status='0')
        return render(request, 'order/order_waitpay.html', {'orders':orders})


# 待收货订单页面
def order_paid(request):
    userid = request.session.get('userid', '')
    if not userid:
        return redirect(reverse('App:login_handle'))
    else:
        # 如果登录了，则获取到当前用户下的所有待收货订单
        orders = Order.objects.filter(user_id=userid, order_status='1')
        return render(request, 'order/order_paid.html', {'orders': orders})
