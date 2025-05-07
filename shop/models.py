from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime

from django.urls import reverse


class Section(models.Model):
    title = models.CharField(
        max_length=70,
        help_text="В поле необходимо ввести название раздела",
        unique=True,
        verbose_name="Название раздела"
    )
    """Создание verbose_name="Название раздела" для ЧПУ ссылки"""
    slug = models.SlugField(max_length=40, verbose_name="Псевдоним", default="")

    class Meta:
        ordering = ["id"]
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    # def get_absolute_url(self):
    #     print(f"dfdfd", reverse("section", args=[self.id]))
    #     return reverse("section", args=[self.id])
        # return reverse("section", args=[self.id])

        # < a href = "{% url 'section' %}" > {{section.title}} < / a >

    def __str__(self):
        return self.title


class Product(models.Model):
    section = models.ForeignKey("Section", on_delete=models.SET_NULL, null=True, verbose_name = "Раздел")
    title = models.CharField(
        max_length=70,
        help_text="В поле необходимо ввести название раздела",
        unique=True,
        verbose_name="Название"
    )
    image = models.ImageField(upload_to="images", verbose_name="Изображение", null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", null=True)
    year = models.IntegerField(null=True, validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)])
    country = models.CharField(max_length=70, verbose_name="Страна", null=True, blank=True)
    director = models.CharField(max_length=70, verbose_name="Режиссер", null=True, blank=True)
    play = models.IntegerField(null=True,
                               blank=True,
                               verbose_name="Продолжительность",
                               help_text="В секундах",
                               validators=[MinValueValidator(60)]
                               )
    cast = models.TextField(verbose_name="В ролях", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    date = models.DateField(auto_now_add=True, verbose_name="Дата", null=True, blank=True)
    slug = models.SlugField(max_length=40, verbose_name="Псевдоним", default="")
    count = 1

    class Meta:
        ordering = ["title"]
        # ordering = ["title", "year"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def get_count(self):
        return self.count

    def get_sum_price(self):
        return self.count * self.price

    def __str__(self):
        return "{0} ({1})".format(self.title, self.section)


class Discount(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Код купона")
    value = models.IntegerField(null=True,
                               blank=True,
                               verbose_name="Размер скидки",
                               help_text="В процентах",
                               validators=[MinValueValidator(0), MaxValueValidator(100)]
                               )

    class Meta:
        ordering = ["-value"]
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def value_percent(self):
        return str(self.value) + "%"

    def __str__(self):
        return self.code
        # return self.code + " (" + str(self.value) + "%)"

    value_percent.short_description = "Размер скидки"


class Order(models.Model):
    need_delivery = models.BooleanField(verbose_name="Необходимость доставки")
    discount = models.ForeignKey(Discount, verbose_name="Скидка", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=70, verbose_name="Имя клиента")
    phone = models.CharField(max_length=70, verbose_name="Телефон клиента")
    email = models.EmailField()
    address = models.TextField(verbose_name="Адрес", blank=True)
    notice = models.TextField(max_length=150, verbose_name="Примечание", blank=True)
    date_order = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    date_send = models.DateTimeField(blank=True, null=True, verbose_name="Дата отправки")

    STATUSES = [
        ("NEW", "Новый заказ"),
        ("APR", "Подтвержден"),
        ("PAY", "Оплачен"),
        ("CNL", "Отменен"),
    ]

    status = models.CharField(choices=STATUSES, max_length=3, default="NEW", verbose_name="Статус")

    class Meta:
        ordering = ["-date_order"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        """Добавление разрешения на смену статуса"""
        permissions = (("can_set_status", "возможность настройки статуса"),)

    def display_products(self):
        display = ""
        for order_line in self.orderline_set.all():
            display += "{0}: {1}шт.; ".format(order_line.product.title, order_line.count)
        return display

    def display_amount(self):
        amount = 0
        for order_line in self.orderline_set.all():
            amount += order_line.product.price * order_line.count

        if self.discount:
            amount = round(amount * Decimal(1 - self.discount.value / 100))
        return "{0} руб.".format(amount)

    def __str__(self):
        # return "ID" + str(self.id)
        return self.name

    display_products.short_description = "Состав заказа"
    display_amount.short_description = "Сумма"

class OrderLine(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", default=0)
    count = models.IntegerField(verbose_name="Количество", validators=[MinValueValidator(1)], default=1)

    class Meta:
        verbose_name = "Стока заказа"
        verbose_name_plural = "Строки заказа"

    def __str__(self):
        return "Заказ (ID {0}) {1}: {2}шт.".format(self.order.id, self.product.title, self.count)
    # asdf123!@