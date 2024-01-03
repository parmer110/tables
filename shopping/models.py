from django.db import models
from common.models import Person, Places, CommonModel
from treatment.models import Customer


class Product(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Purchase(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='PurchaseItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Purchase by {self.customer}'

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'


class PurchaseItem(CommonModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product}'

    class Meta:
        verbose_name = 'Purchase Item'
        verbose_name_plural = 'Purchase Items'


