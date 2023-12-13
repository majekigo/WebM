from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название тега')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    categories = models.ManyToManyField(Category, verbose_name='Категории')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.AutoField(primary_key=True, verbose_name='Номер заказа')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    delivery_address = models.TextField(verbose_name='Адрес доставки')
    customer_phone = models.CharField(max_length=20, verbose_name='Телефон клиента')
    customer_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    products = models.ManyToManyField(Product, through='OrderPosition', verbose_name='Товары')

    def __str__(self):
        return f'Order #{self.order_number}'


class OrderPosition(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Скидка')

    def __str__(self):
        return f'Order #{self.order.order_number} - Position #{self.id}'
