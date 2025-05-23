import transliterate
from chardet.cli.chardetect import description_of
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import title
from django.template.loader import get_template
from django.urls import reverse
from django.views import generic
from uaclient.http import HTTPResponse

from shop.forms import SearchForm, OrderModelForm
from shop.models import Section, Product, Discount, Order, OrderLine


def index(request):
    products = Product.objects.all()
    for product in products:
        slug = transliterate.translit(product.title, reversed=True)
        slug = slug.replace("'", "")
        slug = slug.replace("?", "")
        slug = slug.replace(":", "")
        slug = slug.replace(".", "")
        slug = slug.replace(",", "")
        slug = slug.replace(" ", "-")
        slug = slug.lower()
        print(slug)
        product.slug = slug
        product.save()
    result = prerender(request)
    if result:
        return result
    products = Product.objects.all().order_by(get_order_by_product(request))[:8]
    context = {"products": products}
    return render(
        request,
        "index.html",
        context=context
    )


def prerender(request):
    if request.GET.get("add_cart"):
        product_id = request.GET.get("add_cart")
        get_object_or_404(Product, pk=product_id)
        cart_info = request.session.get("cart_info", {})
        count = cart_info.get(product_id, 0)
        count += 1
        cart_info.update({product_id: count})
        request.session["cart_info"] = cart_info
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def get_order_by_product(request):
    order_by = ""
    if request.GET.get("sort") and request.GET.get("up"):
        sort = request.GET.get("sort")
        up = request.GET.get("up")
        if sort == "price" or sort == "title":
            if up == "0":
                order_by = "-"
            order_by += sort
    if not order_by:
        order_by = "-date"
    print(f"order_by {order_by}")
    return order_by


def delivery(request):
    # sections = Section.objects.all().order_by("title")
    return render(
        request,
        "delivery.html"
    )


def contacts(request):
    # sections = Section.objects.all().order_by("title")
    return render(
        request,
        "contacts.html"
    )


# def section(request, id):
#     # obj = Section.objects.get(pk=id)
#     obj = get_object_or_404(Section, pk=id)
#     print(f"obj = {obj}")
#     products = Product.objects.filter(section__exact=obj).order_by(get_order_by_product(request))
#     context = {"section": obj, "products": products}
#     return render(
#         request,
#         "section.html",
#         context=context
#     )



class Sections(generic.DetailView):
    model = Section

    def get(self, request, *args, **kwargs):
        result = prerender(request)
        if result:
            return result
        return super(Sections, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        print("1111")
        # print(self.model.id)
        print("222")
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(section__exact=self.object.id).exclude(id=self.get_object().id).order_by('?')[:8]
        return context


class ProductDetailView(generic.DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        result = prerender(request)
        if result:
            return result
        return super(ProductDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["products"] = Product.objects.filter(section__exact=self.get_object().section).\
        exclude(id=self.get_object().id).order_by('?')[:4]
        return context


def handler(request, exception):
    return render(
        request,
        "404.html",
        status=404,
    )


def search(request):
    result = prerender(request)
    if result:
        return result
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        q = search_form.cleaned_data["q"]
        print(q)
        products = Product.objects.filter(
            Q(title__icontains=q) | Q(country__icontains=q) | Q(director__icontains=q) |
            Q(cast__icontains=q) | Q(description__icontains=q)
        )
        page = request.GET.get("page", 1)
        paginator = Paginator(products, 8)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = {"products": products, "q": q}
        return render(
            request,
            "search.html",
            context=context,
        )


def cart(request):
    result = update_cart_info(request)
    if result:
        return result
    cart_info = request.session.get("cart_info")
    products = []
    if cart_info:
        for product_id in cart_info:
            # product = get_object_or_404(Product, pk=product_id)
            try:
                product = Product.objects.get(pk=product_id)
                product.count = cart_info[product_id]
                products.append(product)
            except Product.DoesNotExists:
                raise Http404()
    context = {"products": products, "discount": request.session.get("discount", "")}
    return render(
        request,
        "cart.html",
        context=context,
    )


def update_cart_info(request):
    if request.POST:
        cart_info = {}
        for param in request.POST:
            value = request.POST.get(param)
            if param.startswith("count_") and value.isnumeric():
                product_id = param.replace("count_", "")
                get_object_or_404(Product, pk=product_id)
                cart_info[product_id] = int(value)
            if param.startswith("discount") and value:
                try:
                    discount = Discount.objects.get(code__exact=value)
                    request.session["discount"] = value
                except Discount.DoesNotExist:
                    pass
        request.session["cart_info"] = cart_info

    if request.GET.get("delete_cart"):
        cart_info = request.session.get("cart_info")
        product_id = request.GET.get("delete_cart")
        get_object_or_404(Product, pk=product_id)
        current_count = cart_info.get(product_id, 0)
        if current_count <= 1:
            cart_info.pop(product_id)
        else:
            cart_info[product_id] -= 1
        request.session["cart_info"] = cart_info
        return HttpResponseRedirect(reverse("cart"))


def order(request):
    cart_info = request.session.get("cart_info")
    """Если в заказе ничего нет мы не должны выходить на страницу формы"""
    if not cart_info:
        form = OrderModelForm(request.POST, prefix='form1')
        context = {"form": form}
        return render(
            request,
            "order.html",
            context=context,
        )
        # raise Http404()
    if request.method == "POST":
        form = OrderModelForm(request.POST, prefix='form1')
        if form.is_valid:
            """Получение данных из формы"""
            order_obj = Order()
            order_obj.need_delivery = True if form['delivery'] == 1 else False
            # order_obj.need_delivery = True
            discount_code = request.session.get("discount", "")
            if discount_code:
                try:
                    discount = Discount.object.get(code__exact=discount_code)
                    order_obj.discount = discount
                except Discount.DoesNotExist:
                    pass
            # order_obj.name = form.cleaned_data.get('name')
            # order_obj.phone = form.cleaned_data.get('phone')
            # order_obj.email = form.cleaned_data.get('email')
            # order_obj.address = form.cleaned_data.get('address')
            # order_obj.notice = form.cleaned_data.get('notice')
            order_obj.name = form['name']
            order_obj.phone = form['phone']
            order_obj.email = form['email']
            order_obj.address = form['address']
            order_obj.notice = form['notice']
            order_obj.save()
            add_order_lines(request, order_obj)
            add_user(form['name'], form['email'])
            return HttpResponseRedirect(reverse("addorder"))
    else:
        form = OrderModelForm()
    context = {"form": form}
    return render(
        request,
        "order.html",
        context=context,
    )


def add_order_lines(request, order_obj):
    cart_info = request.session.get("cart_info", {})
    for key in cart_info:
        order_line = OrderLine()
        order_line.order = order_obj
        order_line.product = get_object_or_404(Product, pk=key)
        order_line.price = order_line.product.price
        order_line.count = cart_info[key]
        order_line.save()
    """Удалим содержимое корзины"""
    del request.session["cart_info"]
    # request.session.clear() # Стирает весь кэш и авторизацию тоже


def addorder(request):
    return render(
        request,
        "addorder.html",
    )


def add_user(name, email):
    """Проверка наличия пользователя в базе данных"""
    if User.objects.filter(email=email).exists():
        return

    """Добавление пользователя в базу данных по email"""
    password = User.objects.make_random_password()
    user = User.objects.create_user(email, password)
    user.first_name = name
    group = Group.objects.get(name="Клиенты")
    user.groups.add(group)
    user.save()

    """Отправка письма на электронную почту пользователя о регистрации его в базе данных"""
    text = get_template("registration/registration_email.html")
    html = get_template("registration/registration_email.html")
    context = {"email": email, "password": password}

    subject = "Регирстрация"
    from_email = "from@storedvd.ru"
    text_content = text.render(context)
    html_content = html.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


"""Требование. Только авторизованные пользователи могут зайти на эту страницу"""
@login_required
def orders(request):
    user_orders =Order.objects.filter(email__exact=request.user.email)
    return render(
        request,
        "orders.html",
        context={"orders": user_orders}
    )


"""Требование. Только пользователи с возможностью изменения статуса заказа 
могут зайти на эту страницу"""
@permission_required("shop.can_set_status")
def cancelorder(request, id):
    print(request.user.has_perm("shop.can_set_status"))
    order_obj = get_object_or_404(Order, pk=id)
    if order_obj.email == request.user.email and order_obj.status == "NEW":
        order_obj.status = "CNL"
        order_obj.save()
    return HttpResponseRedirect(reverse("orders"))