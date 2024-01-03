from django.db import models
from common.utils.crypto import encoder, decoder
from common.models import Person, Places, CommonModel, Document, User

class Cost(CommonModel):
    _title = models.CharField(max_length=366+16*100, db_column="title", verbose_name="Title", null=True)
    _amount = models.CharField(max_length=366+16*10, db_column="amount", verbose_name="Amount", null=True)
    _description = models.TextField(db_column="description", verbose_name="Description", null=True)
    vat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Vat", default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Discount", default=0)
    invoice_number = models.CharField(max_length=50, verbose_name="Invoice Number", null=True)
    document = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.invoice_number}"

    @property
    def title(self):
        return decoder(self._title)
    @property
    def amount(self):
        return decoder(self._amount)
    @property
    def description(self):
        return decoder(self._description)

    @title.setter
    def title(self, value):
        self._title = value
    @amount.setter
    def amount(self, value):
        self._amount = value
    @description.setter
    def description(self, value):
        self._description = value

    def save(self, *args, **kwargs):
        self.title = encoder(self.title)
        self.amount= encoder(self.lastname)
        self.description = encoder(self.description)
        super(Cost, self).save(*args, **kwargs)


# مدل برای ثبت اطلاعات تراکنش‌های مالی
class FinancialTransaction(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ")
    description = models.TextField(verbose_name="توضیحات")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.date}"


# مدل برای ثبت اطلاعات خریدها
class Purchase(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    product_name = models.CharField(max_length=100, verbose_name="نام محصول")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ خرید")
    quantity = models.IntegerField(verbose_name="تعداد")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت کل")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    def __str__(self):
        return f"{self.user} - {self.product_name} - {self.amount} - {self.total_price} - {self.date}"

# مدل برای ثبت اطلاعات تنخواه‌ها
class Allowance(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ تنخواه")
    date = models.DateField(verbose_name="تاریخ تنخواه")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.date}"

# مدل برای ثبت اطلاعات هزینه‌ها
class Expense(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(max_length=100, verbose_name="عنوان هزینه")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")
    description = models.TextField(verbose_name="توضیحات")

    def __str__(self):
        return f"{self.user} - {self.title} - {self.amount} - {self.date}"


# مدل برای ثبت اطلاعات پرداخت‌ها
class Payment(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ پرداخت")
    date = models.DateField(verbose_name="تاریخ پرداخت")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.date}"


# مدل برای ثبت اطلاعات بودجه‌ها
class Budget(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    name = models.CharField(max_length=100, verbose_name="نام بودجه")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ بودجه")
    start_date = models.DateField(verbose_name="تاریخ شروع بودجه")
    end_date = models.DateField(verbose_name="تاریخ پایان بودجه")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    def __str__(self):
        return f"{self.user} - {self.name} - {self.amount}"

class FinancialParameter(CommonModel):
    name = models.CharField(max_length=100, verbose_name="نام پارامتر مالی")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مقدار")

    def __str__(self):
        return f"{self.name} - {self.value}"


class Transaction(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان تراکنش")
    category = models.CharField(max_length=100, verbose_name="دسته‌بندی")

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.timestamp}"



# مدل برای ثبت اطلاعات دریافت‌ها
class Income(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ دریافت")
    date = models.DateField(verbose_name="تاریخ دریافت")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.date}"