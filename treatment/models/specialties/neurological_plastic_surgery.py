from django.db import models

name = "Neurological Plastic Surgery"

# مدل بیمار
class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    # دیگر فیلدهای مربوط به بیمار
    # ...

# مدل تخصص جراحی پلاستیک عصبی (Neurological Plastic Surgery)
class NeurologicalPlasticSurgery(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nerve_repair_techniques = models.TextField(verbose_name='تکنیک‌های تعمیر عصب')
    cranial_reconstruction_techniques = models.TextField(verbose_name='تکنیک‌های بازسازی مغزی')
    spine_reconstruction_techniques = models.TextField(verbose_name='تکنیک‌های بازسازی اسپینال')
    # دیگر فیلدهای مربوط به تخصص جراحی پلاستیک عصبی
    # ...

# مدل تجویز (Treatment)
class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    # دیگر فیلدهای مربوط به تجویز
    # ...
