import os
import glob
import re
import io

def rename_models_in_specialties1():
    # نام اپلیکیشن
    app_name = "treatment"
    # مسیر پوشه ای که ماژول‌های تخصص‌ها در آن قرار دارند
    specialties_dir = os.path.join(app_name, "models", "TEMP")

    # خواندن فایل‌های ماژول‌ها از پوشه "specialties"
    module_files = glob.glob(os.path.join(specialties_dir, "*.py"))

    # حذف فایل __init__.py از فهرست فایل‌های خوانده شده
    module_files = [file for file in module_files if not os.path.basename(file).startswith("__init__")]

    for module_file in module_files:
        # استخراج نام ماژول از آدرس فایل
        module_name = os.path.basename(module_file).replace(".py", "")

        # فتح فایل ماژول و خواندن محتوای آن با استفاده از کتابخانه io
        with io.open(module_file, "r", encoding="utf-8") as f:
            module_content = f.read()

        # اعمال الگوی جستجو بر روی محتوای ماژول
        updated_module_content = re.sub(r"(class\s+Patient\(models\.Model\):)", r"\1\n    class Meta:\n        db_table = '{}_Patient'".format(module_name), module_content)
        updated_module_content = re.sub(r"(class\s+Treatment\(models\.Model\):)", r"\1\n    class Meta:\n        db_table = '{}_Treatment'".format(module_name), updated_module_content)

        # نوشتن محتوای به‌روز شده در فایل ماژول با استفاده از کتابخانه io
        with io.open(module_file, "w", encoding="utf-8") as f:
            f.write(updated_module_content)




def rename_models_in_specialties2():
        # نام اپلیکیشن
    app_name = "treatment"
    # مسیر پوشه ای که ماژول‌های تخصص‌ها در آن قرار دارند
    specialties_dir = os.path.join(app_name, "models", "TEMP")

    # خواندن فایل‌های ماژول‌ها از پوشه "specialties"
    module_files = glob.glob(os.path.join(specialties_dir, "*.py"))

    # حذف فایل __init__.py از فهرست فایل‌های خوانده شده
    module_files = [file for file in module_files if not os.path.basename(file).startswith("__init__")]

    for module_file in module_files:
        # استخراج نام ماژول از آدرس فایل
        module_name = os.path.basename(module_file).replace(".py", "")

        # فتح فایل ماژول و خواندن محتوای آن با استفاده از کتابخانه io
        with io.open(module_file, "r", encoding="utf-8") as f:
            module_content = f.read()

        # اضافه کردن import جدید به بالای ماژول
        updated_module_content = module_content.replace("from django.db import models", "from django.db import models\nfrom common.models import Person, Places, CommonModel")

        # تغییر نام مدل‌های Patient و Treatment با توجه به نام ماژول
        updated_module_content = re.sub(r"(class\s+Patient\(models\.Model\):)", r"class {}_Patient(models.Model):".format(module_name), updated_module_content)
        updated_module_content = re.sub(r"(class\s+Treatment\(models\.Model\):)", r"class {}_Treatment(models.Model):".format(module_name), updated_module_content)

        # تغییر نام مدل‌های ارجا به مدل‌های جدید
        updated_module_content = re.sub(r"\bPatient\b", "{}_Patient".format(module_name), updated_module_content)
        updated_module_content = re.sub(r"\bTreatment\b", "{}_Treatment".format(module_name), updated_module_content)

        # نوشتن محتوای به‌روز شده در فایل ماژول با استفاده از کتابخانه io
        with io.open(module_file, "w", encoding="utf-8") as f:
            f.write(updated_module_content)


def rename_models_in_specialties3():
        # نام اپلیکیشن
    app_name = "treatment"
    # مسیر پوشه ای که ماژول‌های تخصص‌ها در آن قرار دارند
    specialties_dir = os.path.join(app_name, "models", "specialties")

    # خواندن فایل‌های ماژول‌ها از پوشه "specialties"
    module_files = glob.glob(os.path.join(specialties_dir, "*.py"))

    # حذف فایل __init__.py از فهرست فایل‌های خوانده شده
    module_files = [file for file in module_files if not os.path.basename(file).startswith("__init__")]

    for module_file in module_files:

        # فتح فایل ماژول و خواندن محتوای آن با استفاده از کتابخانه io
        with io.open(module_file, "r", encoding="utf-8") as f:
            module_content = f.read()

        # تغییر نام مدل‌های Patient و Treatment با توجه به نام ماژول
        updated_module_content = re.sub(r"(\(models\.Model\):)", r"({}):".format("CommonModel"), module_content)

        # نوشتن محتوای به‌روز شده در فایل ماژول با استفاده از کتابخانه io
        with io.open(module_file, "w", encoding="utf-8") as f:
            f.write(updated_module_content)


# اجرای تابع برای اصلاح نام مدل‌ها در ماژول‌ها
# rename_models_in_specialties1()

# اجرای تابع برای اصلاح نام مدل‌ها در ماژول‌ها
# rename_models_in_specialties2()

# اجرای تابع برای اصلاح نام مدل‌ها در ماژول‌ها
rename_models_in_specialties3()
