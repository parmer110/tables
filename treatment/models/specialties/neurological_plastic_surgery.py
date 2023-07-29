from django.db import models
from common.models import Person, Places, CommonModel

name = "Neurological Plastic Surgery"

# مدل بیمار
class neurological_plastic_surgery_Patient(CommonModel):
    class Meta:
        db_table = 'neurological_plastic_surgery_Patient'
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    # دیگر فیلدهای مربوط به بیمار
    # ...

# مدل تخصص جراحی پلاستیک عصبی (Neurological Plastic Surgery)
class NeurologicalPlasticSurgery(CommonModel):
    patient = models.ForeignKey(neurological_plastic_surgery_Patient, on_delete=models.CASCADE)
    nerve_repair_techniques = models.TextField(verbose_name='تکنیک‌های تعمیر عصب')
    cranial_reconstruction_techniques = models.TextField(verbose_name='تکنیک‌های بازسازی مغزی')
    spine_reconstruction_techniques = models.TextField(verbose_name='تکنیک‌های بازسازی اسپینال')
    # دیگر فیلدهای مربوط به تخصص جراحی پلاستیک عصبی
    # ...

# مدل تجویز (neurological_plastic_surgery_Treatment)
class neurological_plastic_surgery_Treatment(CommonModel):
    class Meta:
        db_table = 'neurological_plastic_surgery_Treatment'
    patient = models.ForeignKey(neurological_plastic_surgery_Patient, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    # دیگر فیلدهای مربوط به تجویز
    # ...
