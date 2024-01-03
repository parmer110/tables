import docx
import re
from django.core.management.base import BaseCommand
from common.models import Translate, FieldOfStudy, Classification, EducationalDegree, SettingMenus
from treatment.models import Specialty, Procedure
from financialhub.models import Cost

class Command(BaseCommand):
    help = 'Import medical specialties and sub-specialties from a Word file'

    def handle(self, *args, **kwargs):
        # read the Word file
        doc = docx.Document('C:/Users/User/Documents/Work/Ramin/specialists.docx')

        # iterate through the paragraphs in the Word file
        for paragraph in doc.paragraphs:
            # find all occurrences of numbers followed by a '-' character
            matches = re.findall(r'\d+-', paragraph.text)

            # check if there is only one match
            if len(matches) == 1:
                # split the paragraph by the '-' character
                parts = paragraph.text.split('-')

                # get the Persian and English names
                persian_name = parts[-2].strip()
                english_name = parts[-1].strip().replace('(', '').replace(')', '')

                # create a new Translate object and save it to the database
                Translate.objects.create(Persian=persian_name, English=english_name)

        # print a message indicating successful import
        print('Medical specialties and sub-specialties have been imported successfully.')


def translateImport01():
    specialties = [
        {
            "persian": "آلرژی و ایمونولوژی",
            "english": "Allergy and Immunology",
            "arabic": "الربو و المناعة",
            "russian": "Аллергология и иммунология",
            "chineseTraditional": "過敏和免疫學",
            "spanish": "Alergia e inmunología"
        },
        {
            "persian": "بیهوشی",
            "english": "Anesthesiology",
            "arabic": "تخدير",
            "russian": "Анестезиология",
            "chineseTraditional": "麻醉學",
            "spanish": "Anestesiología"
        },
        {
            "persian": "پوست",
            "english": "Dermatology",
            "arabic": "طب الجلد",
            "russian": "Дерматология",
            "chineseTraditional": "皮膚科學",
            "spanish": "Dermatología"
        },
        {
            "persian": "رادیولوژی تشخیصی",
            "english": "Diagnostic Radiology",
            "arabic": "تصوير الاشعة",
            "russian": "Диагностическая радиология",
            "chineseTraditional": "診斷放射學",
            "spanish": "Radiología diagnóstica"
        },
        {
            "persian": "پزشکی اورژانس",
            "english": "Emergency Medicine",
            "arabic": "طب الطوارئ",
            "russian": "Экстренная медицина",
            "chineseTraditional": "急診醫學",
            "spanish": "Medicina de emergencia"
        },
        {
            "persian": "پزشکی خانواده",
            "english": "Family Medicine",
            "arabic": "طب العائلة",
            "russian": "Семейная медицина",
            "chineseTraditional": "家庭醫學",
            "spanish": "Medicina de familia"
        },
        {
            "persian": "پزشکی داخلی",
            "english": "Internal Medicine",
            "arabic": "طب الباطنية",
            "russian": "Терапия",
            "chineseTraditional": "內科學",
            "spanish": "Medicina interna"
        },
        {
            "persian": "ژنتیک پزشکی",
            "english": "Medical Genetics",
            "arabic": "طب الأمراض الوراثية",
            "russian": "Медицинская генетика",
            "chineseTraditional": "醫學遺傳學",
            "spanish": "Genética médica"
        },
        {
            "persian": "عصب‌شناسی",
            "english": "Neurology",
            "arabic": "أمراض الأعصاب",
            "russian": "Неврология",
            "chineseTraditional": "神經學",
            "spanish": "Neurología"
        },
        {
            "persian": "پزشکی هسته‌ای",
            "english": "Nuclear Medicine",
            "arabic": "الطب النووي",
            "russian": "Ядерная медицина",
            "chineseTraditional": "核醫學",
            "spanish": "Medicina nuclear"
        },
    ]
    for specialty in specialties:
        Translate.objects.create(
            persian=specialty["persian"],
            english=specialty["english"],
            arabic=specialty["arabic"],
            russian=specialty["russian"],
            chineseTraditional=specialty["chineseTraditional"],
            spanish=specialty["spanish"]
        )


def translateImport02():
    specialties = [
        {
            "persian": "آلرژی و ایمونولوژی",
            "english": "Allergy and Immunology",
            "arabic": "الربو و المناعة",
            "russian": "Аллергология и иммунология",
            "chineseTraditional": "過敏和免疫學",
            "spanish": "Alergia e inmunología",
            "french": "Allergie et immunologie",
            "german": "Allergie und Immunologie",
            "italian": "Allergologia e immunologia"
        },
        {
            "persian": "بیهوشی",
            "english": "Anesthesiology",
            "arabic": "تخدير",
            "russian": "Анестезиология",
            "chineseTraditional": "麻醉學",
            "spanish": "Anestesiología",
            "french": "Anesthésiologie",
            "german": "Anästhesiologie",
            "italian": "Anestesiologia"
        },
        {
            "persian": "پوست",
            "english": "Dermatology",
            "arabic": "طب الجلد",
            "russian": "Дерматология",
            "chineseTraditional": "皮膚科學",
            "spanish": "Dermatología",
            "french": "Dermatologie",
            "german": "Dermatologie",
            "italian": "Dermatologia"
        },
        {
            "persian": "رادیولوژی تشخیصی",
            "english": "Diagnostic Radiology",
            "arabic": "التصویر الطبي التشخيصي",
            "russian": "Диагностическая радиология",
            "chineseTraditional": "診斷放射學",
            "spanish": "Radiología de diagnóstico",
            "french": "Radiologie diagnostique",
            "german": "Diagnostische Radiologie",
            "italian": "Radiologia diagnostica"
        },
        {
            "persian": "پزشکی اورژانس",
            "english": "Emergency Medicine",
            "arabic": "طب الطوارئ",
            "russian": "Скорая медицинская помощь",
            "chineseTraditional": "緊急醫學",
            "spanish": "Medicina de emergencia",
            "french": "Médecine d'urgence",
            "german": "Notfallmedizin",
            "italian": "Medicina d'urgenza"
        },
        {
            "persian": "پزشکی خانواده",
            "english": "Family Medicine",
            "arabic": "طب الأسرة",
            "russian": "Семейная медицина",
            "chineseTraditional": "家庭醫學",
            "spanish": "Medicina de familia",
            "french": "Médecine de famille",
            "german": "Familienmedizin",
            "italian": "Medicina di famiglia"
        },
        {
            "persian": "پزشکی داخلی",
            "english": "Internal Medicine",
            "arabic": "الطب الباطني",
            "russian": "Внутренняя медицина",
            "chineseTraditional": "內科學",
            "spanish": "Medicina interna",
            "french": "Médecine interne",
            "german": "Innere Medizin",
            "italian": "Medicina interna"
        },
        {
            "persian": "ژنتیک پزشکی",
            "english": "Medical Genetics",
            "arabic": "الجينات الطبية",
            "russian": "Медицинская генетика",
            "chineseTraditional": "醫學遺傳學",
            "spanish": "Genética médica",
            "french": "Génétique médicale",
            "german": "Medizinische Genetik",
            "italian": "Genetica medica"
        },
        {
            "persian": "عصب‌شناسی",
            "english": "Neurology",
            "arabic": "علم الأعصاب",
            "russian": "Неврология",
            "chineseTraditional": "神經學",
            "spanish": "Neurología",
            "french": "Neurologie",
            "german": "Neurologie",
            "italian": "Neurologia"
        },
        {
            "persian": "پزشکی هسته‌ای",
            "english": "Nuclear Medicine",
            "arabic": "الطب النووي",
            "russian": "Ядерная медицина",
            "chineseTraditional": "核醫學",
            "spanish": "Medicina nuclear",
            "french": "Médecine nucléaire",
            "german": "Nuklearmedizin",
            "italian": "Medicina nucleare"
        },
    ]

    for specialty in specialties:
        Translate.objects.create(
            persian=specialty["persian"],
            english=specialty["english"],
            arabic=specialty["arabic"],
            russian=specialty["russian"],
            chineseTraditional=specialty["chineseTraditional"],
            spanish=specialty["spanish"],
            french=specialty["french"],
            german=specialty["german"],
            italian=specialty["italian"],
        )

def translateImport03():
    specialties = [
    {
        "persian": "زنان و زایمان",
        "english": "Obstetrics and Gynecology",
        "arabic": "طب النساء والتوليد",
        "russian": "Акушерство и гинекология",
        "chineseTraditional": "婦產科學",
        "spanish": "Obstetricia y Ginecología",
        "french": "Obstétrique et gynécologie",
        "german": "Geburtshilfe und Gynäkologie",
        "italian": "Ostetricia e ginecologia"
    },
    {
        "persian": "چشم پزشکی",
        "english": "Ophthalmology",
        "arabic": "طب العيون",
        "russian": "Офтальмология",
        "chineseTraditional": "眼科學",
        "spanish": "Oftalmología",
        "french": "Ophtalmologie",
        "german": "Augenheilkunde",
        "italian": "Oftalmologia"
    },
    {
        "persian": "پاتولوژی",
        "english": "Pathology",
        "arabic": "علم الأمراض",
        "russian": "Патология",
        "chineseTraditional": "病理學",
        "spanish": "Patología",
        "french": "Pathologie",
        "german": "Pathologie",
        "italian": "Patologia"
    },
    {
        "persian": "کودکان",
        "english": "Pediatrics",
        "arabic": "طب الأطفال",
        "russian": "Педиатрия",
        "chineseTraditional": "兒科學",
        "spanish": "Pediatría",
        "french": "Pédiatrie",
        "german": "Kinderheilkunde",
        "italian": "Pediatria"
    },
    {
        "persian": "پزشکی فیزیکال و توانبخشی",
        "english": "Physical Medicine and Rehabilitation",
        "arabic": "الطب الطبيعي وإعادة التأهيل",
        "russian": "Физическая медицина и реабилитация",
        "chineseTraditional": "物理醫學與康復學",
        "spanish": "Medicina Física y Rehabilitación",
        "french": "Médecine physique et réadaptation",
        "german": "Physikalische Medizin und Rehabilitation",
        "italian": "Medicina fisica e riabilitazione"
    },
    {
        "persian": "پزشکی پیشگیرانه",
        "english": "Preventive Medicine",
        "arabic": "الطب الوقائي",
        "russian": "Профилактическая медицина",
        "chineseTraditional": "預防醫學",
        "spanish": "Medicina Preventiva",
        "french": "Médecine préventive",
        "german": "Präventivmedizin",
        "italian": "Medicina preventiva"
    },
    {
        "persian": "روانپزشکی",
        "english": "Psychiatry",
        "arabic": "طب النفسي",
        "russian": "Психиатрия",
        "chineseTraditional": "精神醫學",
        "spanish": "Psiquiatría",
        "french": "Psychiatrie",
        "german": "Psychiatrie",
        "italian": "Psichiatria"
    },
    {
        "persian": "پرتودرمانی و انکولوژی",
        "english": "Radiation Oncology",
        "arabic": "علاج الأورام بالإشعاع",
        "russian": "Лучевая онкология",
        "chineseTraditional": "輻射腫瘤學",
        "spanish": "Oncología Radioterápica",
        "french": "Oncologie radiologique",
        "german": "Strahlentherapie und Onkologie",
        "italian": "Radioterapia oncologica"
    },
    {
        "persian": "جراحی",
        "english": "Surgery",
        "arabic": "جراحة",
        "russian": "Хирургия",
        "chineseTraditional": "外科學",
        "spanish": "Cirugía",
        "french": "Chirurgie",
        "german": "Chirurgie",
        "italian": "Chirurgia"
    },
    {
        "persian": "اورولوژی",
        "english": "Urology",
        "arabic": "المسالك البولية",
        "russian": "Урология",
        "chineseTraditional": "泌尿外科學",
        "spanish": "Urología",
        "french": "Urologie",
        "german": "Urologie",
        "italian": "Urologia"
    }
]

    for specialty in specialties:
        Translate.objects.create(
            persian=specialty["persian"],
            english=specialty["english"],
            arabic=specialty["arabic"],
            russian=specialty["russian"],
            chineseTraditional=specialty["chineseTraditional"],
            spanish=specialty["spanish"],
            french=specialty["french"],
            german=specialty["german"],
            italian=specialty["italian"],
        )

def translateImport04():
    specialties = [
    {
        "persian": "گوارش بالغین",
        "english": "Adult Gastroenterology",
        "arabic": "أمراض الجهاز الهضمي للبالغين",
        "russian": "Гастроэнтерология для взрослых",
        "chineseTraditional": "成人胃腸病學",
        "spanish": "Gastroenterología para adultos",
        "french": "Gastroentérologie adulte",
        "german": "Erwachsenengastroenterologie",
        "italian": "Gastroenterologia per adulti"
    },
    {
        "persian": "گوارش کودکان",
        "english": "Pediatric Gastroenterology",
        "arabic": "أمراض الجهاز الهضمي الأطفال",
        "russian": "Детская гастроэнтерология",
        "chineseTraditional": "小兒胃腸病學",
        "spanish": "Gastroenterología pediátrica",
        "french": "Gastroentérologie pédiatrique",
        "german": "Kinder-Gastroenterologie",
        "italian": "Gastroenterologia pediatrica"
    },
    {
        "persian": "ریه بالغین",
        "english": "Adult Pulmonology",
        "arabic": "أمراض الجهاز التنفسي للبالغين",
        "russian": "Пульмонология для взрослых",
        "chineseTraditional": "成人肺病學",
        "spanish": "Neumología para adultos",
        "french": "Pneumologie adulte",
        "german": "Erwachsenenpulmonologie",
        "italian": "Pneumologia per adulti"
    },
    {
        "persian": "ریه کودکان",
        "english": "Pediatric Pulmonology",
        "arabic": "أمراض الجهاز التنفسي الأطفال",
        "russian": "Детская пульмонология",
        "chineseTraditional": "小兒肺病學",
        "spanish": "Neumología pediátrica",
        "french": "Pneumologie pédiatrique",
        "german": "Kinderpulmonologie",
        "italian": "Pneumologia pediatrica"
    },
    {
        "persian": "غدد بالغین",
        "english": "Adult Endocrinology",
        "arabic": "أمراض الغدد الصماء للبالغين",
        "russian": "Эндокринология для взрослых",
        "chineseTraditional": "成人內分泌學",
        "spanish": "Endocrinología para adultos",
        "french": "Endocrinologie adulte",
        "german": "Erwachsenenendokrinologie",
        "italian": "Endocrinologia per adulti"
    },
    {
        "persian": "غدد کودکان",
        "english": "Pediatric Endocrinology",
        "arabic": "أمراض الغدد الصماء للأطفال",
        "russian": "Детская эндокринология",
        "chineseTraditional": "小兒內分泌學",
        "spanish": "Endocrinología pediátrica",
        "french": "Endocrinologie pédiatrique",
        "german": "Kinderendokrinologie",
        "italian": "Endocrinologia pediatrica"
    },
    {
        "persian": "عفونی بالغین",
        "english": "Adult Infectious Disease",
        "arabic": "أمراض المعدية للبالغين",
        "russian": "Инфекционные болезни для взрослых",
        "chineseTraditional": "成人傳染病學",
        "spanish": "Enfermedades infecciosas para adultos",
        "french": "Maladies infectieuses adultes",
        "german": "Infektiologie für Erwachsene",
        "italian": "Malattie infettive per adulti"
    },
    {
        "persian": "عفونی کودکان",
        "english": "Pediatric Infectious Disease",
        "arabic": "أمراض المعدية للأطفال",
        "russian": "Инфекционные болезни у детей",
        "chineseTraditional": "小兒傳染病學",
        "spanish": "Enfermedades infecciosas pediátricas",
        "french": "Maladies infectieuses pédiatriques",
        "german": "Infektiologie für Kinder",
        "italian": "Malattie infettive pediatriche"
    },
    {
        "persian": "روماتولوژی بالغین",
        "english": "Adult Rheumatology",
        "arabic": "أمراض المفاصل والتمور للبالغين",
        "russian": "Ревматология для взрослых",
        "chineseTraditional": "成人風濕病學",
        "spanish": "Reumatología para adultos",
        "french": "Rhumatologie adulte",
        "german": "Erwachsenenrheumatologie",
        "italian": "Reumatologia per adulti"
    },
    {
        "persian": "روماتولوژی کودکان",
        "english": "Pediatric Rheumatology",
        "arabic": "أمراض المفاصل والتمور للأطفال",
        "russian": "Детская ревматология",
        "chineseTraditional": "小兒風濕病學",
        "spanish": "Reumatología pediátrica",
        "french": "Rhumatologie pédiatrique",
        "german": "Kinder-Rheumatologie",
        "italian": "Reumatologia pediatrica"
    }
    ]

    for specialty in specialties:
        Translate.objects.create(
            persian=specialty["persian"],
            english=specialty["english"],
            arabic=specialty["arabic"],
            russian=specialty["russian"],
            chineseTraditional=specialty["chineseTraditional"],
            spanish=specialty["spanish"],
            french=specialty["french"],
            german=specialty["german"],
            italian=specialty["italian"],
        )

def translateImport05():
    specialties = [
    {
        "persian": "نفرولوژی بالغین",
        "english": "Adult Nephrology",
        "arabic": "الكلي البالغ",
        "russian": "Взрослая нефрология",
        "chineseTraditional": "成人腎病學",
        "spanish": "Nefrología para adultos",
        "french": "Néphrologie adulte",
        "german": "Erwachsenennephrologie",
        "italian": "Nefrologia per adulti"
    },
    {
        "persian": "نفرولوژی کودکان",
        "english": "Pediatric Nephrology",
        "arabic": "الكلى الأطفال",
        "russian": "Педиатрическая нефрология",
        "chineseTraditional": "小兒腎病學",
        "spanish": "Nefrología pediátrica",
        "french": "Néphrologie pédiatrique",
        "german": "Kindernefrologie",
        "italian": "Nefrologia pediatrica"
    },
    {
        "persian": "هماتولوژی بالغین",
        "english": "Adult Hematology",
        "arabic": "أمراض الدم للبالغين",
        "russian": "Гематология для взрослых",
        "chineseTraditional": "成人血液學",
        "spanish": "Hematología para adultos",
        "french": "Hématologie adulte",
        "german": "Erwachsenenhämatologie",
        "italian": "Ematologia per adulti"
    },
    {
        "persian": "هماتولوژی کودکان",
        "english": "Pediatric Hematology",
        "arabic": "أمراض الدم للأطفال",
        "russian": "Детская гематология",
        "chineseTraditional": "小兒血液學",
        "spanish": "Hematología pediátrica",
        "french": "Hématologie pédiatrique",
        "german": "Kinderhämatologie",
        "italian": "Ematologia pediatrica"
    },
    {
        "persian": "ارتوپدی بالغین",
        "english": "Adult Orthopedics",
        "arabic": "جراحة العظام للبالغين",
        "russian": "Травматология для взрослых",
        "chineseTraditional": "成人骨科學",
        "spanish": "Ortopedia para adultos",
        "french": "Orthopédie adulte",
        "german": "Erwachsenenorthopädie",
        "italian": "Ortopedia per adulti"
    },
    {
        "persian": "ارتوپدی کودکان",
        "english": "Pediatric Orthopedics",
        "arabic": "جراحة العظام للأطفال",
        "russian": "Детская ортопедия",
        "chineseTraditional": "小兒骨科學",
        "spanish": "Ortopedia pediátrica",
        "french": "Orthopédie pédiatrique",
        "german": "Kinderorthopädie",
        "italian": "Ortopedia pediatrica"
    },
    {
        "persian": "گوش و حلق و بینی بالغین",
        "english": "Adult Otolaryngology",
        "arabic": "أمراض الأذن والحنجرة والأنف للبالغين",
        "russian": "ЛОР для взрослых",
        "chineseTraditional": "成人耳鼻喉科學",
        "spanish": "Otorrinolaringología para adultos",
        "french": "Oto-rhino-laryngologie adulte",
        "german": "Erwachsenen-Hals-Nasen-Ohren-Heilkunde",
        "italian": "Otorinolaringoiatria per adulti"
    },
    {
        "persian": "گوش و حلق و بینی کودکان",
        "english": "Pediatric Otolaryngology",
        "arabic": "أمراض الأذن والحنجرة والأنف للأطفال",
        "russian": "Детская оториноларингология",
        "chineseTraditional": "小兒耳鼻喉科學",
        "spanish": "Otorrinolaringología pediátrica",
        "french": "Oto-rhino-laryngologie pédiatrique",
        "german": "Kinder-Hals-Nasen-Ohren-Heilkunde",
        "italian": "Otorinolaringoiatria pediatrica"
    },
    {
        "persian": "جراحی عمومی بالغین",
        "english": "Adult General Surgery",
        "arabic": "جراحة عامة للبالغين",
        "russian": "Общая хирургия для взрослых",
        "chineseTraditional": "成人普通外科學",
        "spanish": "Cirugía general para adultos",
        "french": "Chirurgie générale adulte",
        "german": "Allgemeinchirurgie für Erwachsene",
        "italian": "Chirurgia generale per adulti"
    },
    {
        "persian": "جراحی عمومی کودکان",
        "english": "Pediatric General Surgery",
        "arabic": "جراحة عامة للأطفال",
        "russian": "Детская общая хирургия",
        "chineseTraditional": "小兒普通外科學",
        "spanish": "Cirugía general pediátrica",
        "french": "Chirurgie générale pédiatrique",
        "german": "Kinder-Allgemeinchirurgie",
        "italian": "Chirurgia generale pediatrica"
    },
    ]

    for specialty in specialties:
        Translate.objects.create(
            persian=specialty["persian"],
            english=specialty["english"],
            arabic=specialty["arabic"],
            russian=specialty["russian"],
            chineseTraditional=specialty["chineseTraditional"],
            spanish=specialty["spanish"],
            french=specialty["french"],
            german=specialty["german"],
            italian=specialty["italian"],
        )

def translateImport06():
    specialties = [
    {
        "persian": "جراحی پلاستیک بالغین",
        "english": "Adult Plastic Surgery",
        "arabic": "جراحة تجميل للبالغين",
        "russian": "Пластическая хирургия для взрослых",
        "chineseTraditional": "成人整形外科學",
        "spanish": "Cirugía plástica para adultos",
        "french": "Chirurgie plastique adulte",
        "german": "Plastische Chirurgie für Erwachsene",
        "italian": "Chirurgia plastica per adulti"
    },
    {
        "persian": "جراحی پلاستیک کودکان",
        "english": "Pediatric Plastic Surgery",
        "arabic": "جراحة تجميل للأطفال",
        "russian": "Детская пластическая хирургия",
        "chineseTraditional": "小兒整形外科學",
        "spanish": "Cirugía plástica pediátrica",
        "french": "Chirurgie plastique pédiatrique",
        "german": "Kinderplastische Chirurgie",
        "italian": "Chirurgia plastica pediatrica"
    },
    {
        "persian": "جراحی قلب و عروق بالغین",
        "english": "Adult Cardiovascular Surgery",
        "arabic": "جراحة القلب والأوعية الدموية للبالغين",
        "russian": "Хирургия сердца и сосудов для взрослых",
        "chineseTraditional": "成人心血管外科學",
        "spanish": "Cirugía cardiovascular para adultos",
        "french": "Chirurgie cardiovasculaire adulte",
        "german": "Erwachsenen-Herz-Kreislauf-Chirurgie",
        "italian": "Chirurgia cardiovascolare per adulti"
    },
    {
        "persian": "جراحی قلب و عروق کودکان",
        "english": "Pediatric Cardiovascular Surgery",
        "arabic": "جراحة القلب والأوعية الدموية للأطفال",
        "russian": "Детская хирургия сердца и сосудов",
        "chineseTraditional": "小兒心血管外科學",
        "spanish": "Cirugía cardiovascular pediátrica",
        "french": "Chirurgie cardiovasculaire pédiatrique",
        "german": "Kinder-Herz-Kreislauf-Chirurgie",
        "italian": "Chirurgia cardiovascolare pediatrica"
    },
    {
        "persian": "جراحی مغز و اعصاب بالغین",
        "english": "Adult Neurosurgery",
        "arabic": "جراحة المخ والأعصاب للبالغين",
        "russian": "Нейрохирургия для взрослых",
        "chineseTraditional": "成人神經外科學",
        "spanish": "Neurocirugía para adultos",
        "french": "Neurochirurgie adulte",
        "german": "Erwachsenenneurochirurgie",
        "italian": "Neurochirurgia per adulti"
    },
    {
        "persian": "جراحی مغز و اعصاب کودکان",
        "english": "Pediatric Neurosurgery",
        "arabic": "جراحة المخ والأعصاب للأطفال",
        "russian": "Детская нейрохирургия",
        "chineseTraditional": "小兒神經外科學",
        "spanish": "Neurocirugía pediátrica",
        "french": "Neurochirurgie pédiatrique",
        "german": "Kinderneurochirurgie",
        "italian": "Neurochirurgia pediatrica"
    },
    {
        "persian": "آنکولوژی بالغین",
        "english": "Adult Oncology",
        "arabic": "أورام للبالغين",
        "russian": "Онкология для взрослых",
        "chineseTraditional": "成人腫瘤學",
        "spanish": "Oncología para adultos",
        "french": "Oncologie adulte",
        "german": "Onkologie für Erwachsene",
        "italian": "Oncologia per adulti"
    },
    {
        "persian": "آنکولوژی کودکان",
        "english": "Pediatric Oncology",
        "arabic": "أورام للأطفال",
        "russian": "Детская онкология",
        "chineseTraditional": "小兒腫瘤學",
        "spanish": "Oncología pediátrica",
        "french": "Oncologie pédiatrique",
        "german": "Kinderonkologie",
        "italian": "Oncologia pediatrica"
    },
    {
        "persian": "جراحی سینه",
        "english": "Breast Surgery",
        "arabic": "جراحة الثدي",
        "russian": "Хирургия молочных желез",
        "chineseTraditional": "乳房外科學",
        "spanish": "Cirugía de mama",
        "french": "Chirurgie mammaire",
        "german": "Brustchirurgie",
        "italian": "Chirurgia al seno"
    },
    {
        "persian": "جراحی قفسه سینه",
        "english": "Thoracic Surgery",
        "arabic": "جراحة الصدر",
        "russian": "Грудная хирургия",
        "chineseTraditional": "胸腔外科學",
        "spanish": "Cirugía torácica",
        "french": "Chirurgie thoracique",
        "german": "Thoraxchirurgie",
        "italian": "Chirurgia toracica"
    },
    ]

    for specialty in specialties:
        Translate.objects.create(
            persian=specialty["persian"],
            english=specialty["english"],
            arabic=specialty["arabic"],
            russian=specialty["russian"],
            chineseTraditional=specialty["chineseTraditional"],
            spanish=specialty["spanish"],
            french=specialty["french"],
            german=specialty["german"],
            italian=specialty["italian"],
        )


def translateImport07():
    specialties = [
    {
        "persian": "جراحی دست",
        "english": "Hand Surgery",
        "arabic": "جراحة اليد",
        "russian": "Хирургия руки",
        "chineseTraditional": "手外科",
        "spanish": "Cirugía de mano",
        "french": "Chirurgie de la main",
        "german": "Handchirurgie",
        "italian": "Chirurgia della mano"
    },
    {
        "persian": "جراحی پلاستیک صورت",
        "english": "Facial Plastic Surgery",
        "arabic": "جراحة تجميل الوجه",
        "russian": "Пластическая хирургия лица",
        "chineseTraditional": "面部整形外科學",
        "spanish": "Cirugía plástica facial",
        "french": "Chirurgie plastique faciale",
        "german": "Gesichtsplastische Chirurgie",
        "italian": "Chirurgia plastica facciale"
    },
    {
        "persian": "جراحی پایین شکم",
        "english": "Colorectal Surgery",
        "arabic": "جراحة القولون والمستقيم",
        "russian": "Колоректальная хирургия",
        "chineseTraditional": "結腸直腸外科學",
        "spanish": "Cirugía colorrectal",
        "french": "Chirurgie colorectale",
        "german": "Kolorektale Chirurgie",
        "italian": "Chirurgia colorettale"
    },
    {
        "persian": "جراحی سر و گردن",
        "english": "Head and Neck Surgery",
        "arabic": "جراحة الرأس والرقبة",
        "russian": "Хирургия головы и шеи",
        "chineseTraditional": "頭頸外科學",
        "spanish": "Cirugía de cabeza y cuello",
        "french": "Chirurgie de la tête et du cou",
        "german": "Kopf- und Halschirurgie",
        "italian": "Chirurgia testa e collo"
    },
    {
        "persian": "جراحی عروق",
        "english": "Vascular Surgery",
        "arabic": "جراحة الأوعية الدموية",
        "russian": "Сосудистая хирургия",
        "chineseTraditional": "血管外科學",
        "spanish": "Cirugía vascular",
        "french": "Chirurgie vasculaire",
        "german": "Gefäßchirurgie",
        "italian": "Chirurgia vascolare"
    },
    {
        "persian": "جراحی اعصاب دست",
        "english": "Hand Nerve Surgery",
        "arabic": "جراحة اعصاب اليد",
        "russian": "Хирургия нервов руки",
        "chineseTraditional": "手神經外科學",
        "spanish": "Cirugía de nervios de la mano",
        "french": "Chirurgie des nerfs de la main",
        "german": "Handnervenchirurgie",
        "italian": "Chirurgia del nervo della mano"
    },
    {
        "persian": "جراحی پلاستیک سوختگی",
        "english": "Burn Surgery",
        "arabic": "جراحة الحروق",
        "russian": "Хирургия ожогов",
        "chineseTraditional": "燒傷外科學",
        "spanish": "Cirugía de quemaduras",
        "french": "Chirurgie des brûlures",
        "german": "Brandchirurgie",
        "italian": "Chirurgia delle ustioni"
    },
    {
        "persian": "جراحی پلاستیک ترمیمی",
        "english": "Reconstructive Plastic Surgery",
        "arabic": "جراحة تجميلية ترميمية",
        "russian": "Реконструктивная пластическая хирургия",
        "chineseTraditional": "重建性整形外科學",
        "spanish": "Cirugía plástica reconstructiva",
        "french": "Chirurgie plastique reconstructive",
        "german": "Rekonstruktive Plastische Chirurgie",
        "italian": "Chirurgia plastica ricostruttiva"
    },
    {
        "persian": "جراحی پلاستیک تجمیلی",
        "english": "Cosmetic Plastic Surgery",
        "arabic": "جراحة تجميلية",
        "russian": "Косметическая пластическая хирургия",
        "chineseTraditional": "美容整形外科學",
        "spanish": "Cirugía plástica cosmética",
        "french": "Chirurgie plastique cosmétique",
        "german": "Kosmetische Plastische Chirurgie",
        "italian": "Chirurgia plastica estetica"
    },
    {
        "persian": "جراحی پلاستیک تناسب اندام",
        "english": "Body Contouring Surgery",
        "arabic": "جراحة تصحيح الجسم",
        "russian": "Хирургия контурной пластики тела",
        "chineseTraditional": "身體輪廓整形外科學",
        "spanish": "Cirugía de contorno corporal",
        "french": "Chirurgie de la silhouette",
        "german": "Körperkontur-Chirurgie",
        "italian": "Chirurgia di rimodellamento del corpo"
    },
    ]

    for specialty in specialties:
        Translate.objects.create(
            persian=specialty["persian"],
            english=specialty["english"],
            arabic=specialty["arabic"],
            russian=specialty["russian"],
            chineseTraditional=specialty["chineseTraditional"],
            spanish=specialty["spanish"],
            french=specialty["french"],
            german=specialty["german"],
            italian=specialty["italian"],
        )


def translateImport08():
    specialties = [
    {
        "persian": "جراحی پلاستیک صورت",
        "english": "Craniofacial Surgery",
        "arabic": "جراحة التشوهات الوجهية",
        "russian": "Хирургия лицевых дефектов",
        "chineseTraditional": "顱面外科",
        "spanish": "Cirugía craneofacial",
        "french": "Chirurgie craniofaciale",
        "german": "Kraniofaziale Chirurgie",
        "italian": "Chirurgia craniofacciale"
    },
    {
        "persian": "جراحی پلاستیک دست",
        "english": "Hand Plastic Surgery",
        "arabic": "جراحة تجميلية لليد",
        "russian": "Пластическая хирургия руки",
        "chineseTraditional": "手部整形外科學",
        "spanish": "Cirugía plástica de la mano",
        "french": "Chirurgie plastique de la main",
        "german": "Handplastische Chirurgie",
        "italian": "Chirurgia plastica della mano"
    },
    {
        "persian": "جراحی پلاستیک پوست",
        "english": "Dermatologic Surgery",
        "arabic": "جراحة الأمراض الجلدية",
        "russian": "Дерматологическая хирургия",
        "chineseTraditional": "皮膚外科學",
        "spanish": "Cirugía dermatológica",
        "french": "Chirurgie dermatologique",
        "german": "Dermatologische Chirurgie",
        "italian": "Chirurgia dermatologica"
    },
    {
        "persian": "جراحی پلاستیک پایین شکم",
        "english": "Lower Extremity Plastic Surgery",
        "arabic": "جراحة الأطراف السفلية التجميلية",
        "russian": "Пластическая хирургия нижних конечностей",
        "chineseTraditional": "下肢整形外科學",
        "spanish": "Cirugía plástica de extremidades inferiores",
        "french": "Chirurgie plastique des membres inférieurs",
        "german": "Plastische Chirurgie der unteren Extremitäten",
        "italian": "Chirurgia plastica degli arti inferiori"
    },
    {
        "persian": "جراحی پلاستیک بالای شکم",
        "english": "Upper Extremity Plastic Surgery",
        "arabic": "جراحة الأطراف العلوية التجميلية",
        "russian": "Пластическая хирургия верхних конечностей",
        "chineseTraditional": "上肢整形外科學",
        "spanish": "Cirugía plástica de extremidades superiores",
        "french": "Chirurgie plastique des membres supérieurs",
        "german": "Plastische Chirurgie der oberen Extremitäten",
        "italian": "Chirurgia plastica degli arti superiori"
    },
    {
        "persian": "جراحی پلاستیک تنفسی",
        "english": "Respiratory Plastic Surgery",
        "arabic": "جراحة تجميلية للجهاز التنفسي",
        "russian": "Пластическая хирургия дыхательных путей",
        "chineseTraditional": "呼吸整形外科學",
        "spanish": "Cirugía plástica respiratoria",
        "french": "Chirurgie plastique respiratoire",
        "german": "Atemwegsplastische Chirurgie",
        "italian": "Chirurgia plastica respiratoria"
    },
    {
        "persian": "جراحی پلاستیک گوارشی",
        "english": "Gastrointestinal Plastic Surgery",
        "arabic": "جراحة الجهاز الهضمي التجميلية",
        "russian": "Пластическая хирургия органов пищеварения",
        "chineseTraditional": "消化道整形外科學",
        "spanish": "Cirugía plástica gastrointestinal",
        "french": "Chirurgie plastique gastro-intestinale",
        "german": "Gastrointestinale plastische Chirurgie",
        "italian": "Chirurgia plastica gastrointestinale"
    },
    {
        "persian": "جراحی پلاستیک ادراری",
        "english": "Urogenital Plastic Surgery",
        "arabic": "جراحة الجهاز البولي التجميلية",
        "russian": "Пластическая хирургия мочеполовых органов",
        "chineseTraditional": "泌尿生殖整形外科學",
        "spanish": "Cirugía plástica urogenital",
        "french": "Chirurgie plastique urogénitale",
        "german": "Urogenitale plastische Chirurgie",
        "italian": "Chirurgia plastica urogenitale"
    },
    {
        "persian": "جراحی پلاستیک عصبی",
        "english": "Neurological Plastic Surgery",
        "arabic": "جراحة التجميل العصبية",
        "russian": "Неврологическая пластическая хирургия",
        "chineseTraditional": "神經整形外科學",
        "spanish": "Cirugía plástica neurológica",
        "french": "Chirurgie plastique neurologique",
        "german": "Neurologische plastische Chirurgie",
        "italian": "Chirurgia plastica neurologica"
    },
    {
        "persian": "جراحی پلاستیک سرطان",
        "english": "Oncologic Plastic Surgery",
        "arabic": "جراحة التجميل السرطانية",
        "russian": "Онкологическая пластическая хирургия",
        "chineseTraditional": "腫瘤整形外科學",
        "spanish": "Cirugía plástica oncológica",
        "french": "Chirurgie plastique oncologique",
        "german": "Onkologische plastische Chirurgie",
        "italian": "Chirurgia plastica oncologica"
    },
    ]

    for specialty in specialties:
        Translate.objects.create(
            persian=specialty["persian"],
            english=specialty["english"],
            arabic=specialty["arabic"],
            russian=specialty["russian"],
            chineseTraditional=specialty["chineseTraditional"],
            spanish=specialty["spanish"],
            french=specialty["french"],
            german=specialty["german"],
            italian=specialty["italian"],
        )


def translateImport09():
    specialties = [
    {
        "persian": "جراحی پلاستیک ترمیمی سینه",
        "english": "Breast Reconstruction Surgery",
        "arabic": "جراحة إعادة بناء الثدي",
        "russian": "Хирургия реконструкции груди",
        "chineseTraditional": "乳房重建手術",
        "spanish": "Cirugía de reconstrucción mamaria",
        "french": "Chirurgie de reconstruction mammaire",
        "german": "Brustrekonstruktionschirurgie",
        "italian": "Chirurgia di ricostruzione mammaria"
    },
    {
        "persian": "جراحی پلاستیک تجمیلی سینه",
        "english": "Breast Cosmetic Surgery",
        "arabic": "جراحة تجميل الثدي",
        "russian": "Косметическая хирургия груди",
        "chineseTraditional": "乳房整形手術",
        "spanish": "Cirugía cosmética de mama",
        "french": "Chirurgie esthétique mammaire",
        "german": "Ästhetische Brustchirurgie",
        "italian": "Chirurgia estetica del seno"
    },
    {
        "persian": "جراحی پلاستیک تناسب اندام سینه",
        "english": "Breast Body Contouring Surgery",
        "arabic": "جراحة تصحيح الجسم للثدي",
        "russian": "Хирургия контурной пластики груди",
        "chineseTraditional": "乳房體輪廓整形手術",
        "spanish": "Cirugía de contorno corporal de mama",
        "french": "Chirurgie de remodelage corporel mammaire",
        "german": "Brustkörperkonturierungschirurgie",
        "italian": "Chirurgia di rimodellamento corporeo al seno"
    },
    {
        "persian": "جراحی پلاستیک صورت سینه",
        "english": "Breast Craniofacial Surgery",
        "arabic": "جراحة التشوهات الجمالية للثدي",
        "russian": "Хирургия лицевых дефектов груди",
        "chineseTraditional": "顱面整形手術",
        "spanish": "Cirugía craneofacial de mama",
        "french": "Chirurgie craniofaciale mammaire",
        "german": "Kraniofaziale Brustchirurgie",
        "italian": "Chirurgia craniofacciale del seno"
    },
    {
        "persian": "پزشکی خواب",
        "english": "Sleep Medicine",
        "arabic": "طب النوم",
        "russian": "Сомнология",
        "chineseTraditional": "睡眠醫學",
        "spanish": "Medicina del sueño",
        "french": "Médecine du sommeil",
        "german": "Schlafmedizin",
        "italian": "Medicina del sonno"
    },
    {
        "persian": "پزشکی ورزشی",
        "english": "Sports Medicine",
        "arabic": "طب الرياضة",
        "russian": "Спортивная медицина",
        "chineseTraditional": "運動醫學",
        "spanish": "Medicina deportiva",
        "french": "Médecine du sport",
        "german": "Sportmedizin",
        "italian": "Medicina dello sport"
    },
    {
        "persian": "ماساژ‌تراپیست",
        "english": "Massage Therapist",
        "arabic": "أخصائي تدليك",
        "russian": "Массажист",
        "chineseTraditional": "按摩治療師",
        "spanish": "Terapeuta de masaje",
        "french": "Massothérapeute",
        "german": "Massage-Therapeut",
        "italian": "Terapista del massaggio"
    },
    {
        "persian": "مشاور تغذیه",
        "english": "Nutrition Consultant",
        "arabic": "استشاري تغذية",
        "russian": "Консультант по питанию",
        "chineseTraditional": "營養顧問",
        "spanish": "Consultor de nutrición",
        "french": "Conseiller en nutrition",
        "german": "Ernährungsberater",
        "italian": "Consulente nutrizionale"
    },
    {
        "persian": "مددکار اجتماعی در حوزه سلامت",
        "english": "Healthcare Social Worker",
        "arabic": "عامل اجتماعي في مجال الرعاية الصحية",
        "russian": "Социальный работник в здравоохранении",
        "chineseTraditional": "健康照護社會工作者",
        "spanish": "Trabajador social de atención médica",
        "french": "Travailleur social en santé",
        "german": "Sozialarbeiter im Gesundheitswesen",
        "italian": "Assistente sociale sanitario"
    },
    {
        "persian": "مربی تناسب اندام",
        "english": "Fitness Trainer",
        "arabic": "مدرب لياقة بدنية",
        "russian": "Тренер по фитнесу",
        "chineseTraditional": "健身教練",
        "spanish": "Entrenador de fitness",
        "french": "Entraîneur de fitness",
        "german": "Fitness-Trainer",
        "italian": "Allenatore di fitness"
    }
    ]

    for specialty in specialties:
        Translate.objects.create(
            persian=specialty["persian"],
            english=specialty["english"],
            arabic=specialty["arabic"],
            russian=specialty["russian"],
            chineseTraditional=specialty["chineseTraditional"],
            spanish=specialty["spanish"],
            french=specialty["french"],
            german=specialty["german"],
            italian=specialty["italian"],
        )


def translateImport10():
    specialties = [
    {
        "persian": "متخصص تراپی رفتاری",
        "english": "Behavioral Therapy Specialist",
        "arabic": "اختصاصي علاج السلوك",
        "russian": "Специалист по поведенческой терапии",
        "chineseTraditional": "行為療法專家",
        "spanish": "Especialista en terapia conductual",
        "french": "Spécialiste en thérapie comportementale",
        "german": "Verhaltenstherapie-Spezialist",
        "italian": "Specialista in terapia comportamentale"
    },
    {
        "persian": "متخصص یوگا و مراقبت از روحیه",
        "english": "Yoga and Mindfulness Specialist",
        "arabic": "اختصاصي اليوغا والاستيقاظ",
        "russian": "Специалист по йоге и осознанности",
        "chineseTraditional": "瑜伽和正念專家",
        "spanish": "Especialista en yoga y atención plena",
        "french": "Spécialiste en yoga et pleine conscience",
        "german": "Yoga- und Achtsamkeitsspezialist",
        "italian": "Specialista in yoga e consapevolezza"
    },
    {
        "persian": "متخصص تمرینات تنفسی",
        "english": "Breathing Exercise Specialist",
        "arabic": "اختصاصي تمارين التنفس",
        "russian": "Специалист по дыхательным упражнениям",
        "chineseTraditional": "呼吸運動專家",
        "spanish": "Especialista en ejercicios de respiración",
        "french": "Spécialiste des exercices de respiration",
        "german": "Atemübungsspezialist",
        "italian": "Specialista in esercizi di respirazione"
    },
    {
        "persian": "متخصص روان‌شناسی سلامت",
        "english": "Health Psychology Specialist",
        "arabic": "اختصاصي علم النفس الصحي",
        "russian": "Специалист по психологии здоровья",
        "chineseTraditional": "健康心理學專家",
        "spanish": "Especialista en psicología de la salud",
        "french": "Spécialiste en psychologie de la santé",
        "german": "Gesundheitspsychologie-Spezialist",
        "italian": "Specialista in psicologia della salute"
    },
    {
        "persian": "متخصص بهداشت دهان و دندان",
        "english": "Dental Hygiene Specialist",
        "arabic": "اختصاصي نظافة الفم والأسنان",
        "russian": "Специалист по гигиене полости рта",
        "chineseTraditional": "口腔衛生專家",
        "spanish": "Especialista en higiene dental",
        "french": "Spécialiste en hygiène dentaire",
        "german": "Spezialist für Mundhygiene",
        "italian": "Specialista in igiene dentale"
    },
    {
        "persian": "متخصص تغذیه و رژیم غذایی",
        "english": "Nutrition and Dietetics Specialist",
        "arabic": "اختصاصي التغذية والتغذية",
        "russian": "Специалист по питанию и диетологии",
        "chineseTraditional": "營養與營養專家",
        "spanish": "Especialista en nutrición y dietética",
        "french": "Spécialiste en nutrition et diététique",
        "german": "Ernährungs- und Diätetikspezialist",
        "italian": "Specialista in nutrizione e dietetica"
    },
    {
        "persian": "متخصص بهداشت دهان و دندان",
        "english": "Dental Hygiene Specialist",
        "arabic": "اختصاصي نظافة الفم والأسنان",
        "russian": "Специалист по гигиене полости рта",
        "chineseTraditional": "口腔衛生專家",
        "spanish": "Especialista en higiene dental",
        "french": "Spécialiste en hygiène dentaire",
        "german": "Spezialist für Mundhygiene",
        "italian": "Specialista in igiene dentale"
    },
    {
        "persian": "مشاور تغذیه",
        "english": "Nutrition Consultant",
        "arabic": "مستشار التغذية",
        "russian": "Консультант по питанию",
        "chineseTraditional": "營養顧問",
        "spanish": "Consultor de nutrición",
        "french": "Conseiller en nutrition",
        "german": "Ernährungsberater",
        "italian": "Consulente nutrizionale"
    },
    {
        "persian": "تکنولوژی پزشکی",
        "english": "Medical Technology",
        "arabic": "تكنولوجيا الطبية",
        "russian": "Медицинская техника",
        "chineseTraditional": "醫療技術",
        "spanish": "Tecnología médica",
        "french": "Technologie médicale",
        "german": "Medizintechnik",
        "italian": "Tecnologia medica"
    },
    {
        "persian": "پزشکی تله‌مدیسین",
        "english": "Telemedicine",
        "arabic": "الطب عن بعد",
        "russian": "Телемедицина",
        "chineseTraditional": "遠程醫學",
        "spanish": "Telemedicina",
        "french": "Télémédecine",
        "german": "Telemedizin",
        "italian": "Telemedicina"
    },
    {
        "persian": "پزشکی فضایی",
        "english": "Aerospace Medicine",
        "arabic": "طب الفضاء",
        "russian": "Аэрокосмическая медицина",
        "chineseTraditional": "航空太空醫學",
        "spanish": "Medicina aeroespacial",
        "french": "Médecine aérospatiale",
        "german": "Luft- und Raumfahrtmedizin",
        "italian": "Medicina aerospaziale"
    }
    ]

    for specialty in specialties:
        Translate.objects.create(
            persian=specialty["persian"],
            english=specialty["english"],
            arabic=specialty["arabic"],
            russian=specialty["russian"],
            chineseTraditional=specialty["chineseTraditional"],
            spanish=specialty["spanish"],
            french=specialty["french"],
            german=specialty["german"],
            italian=specialty["italian"],
        )

def translateImport11():
    fields = [
        {
            "name": "Theoretical Sciences",
            "sub_class": None,
            "model": None,
            "type": "Academic",
            "description": "This category includes theoretical sciences such as mathematics, theoretical physics, philosophy, and computational sciences."
        },
        {
            "name": "Engineering Sciences",
            "sub_class": None,
            "model": None,
            "type": "Academic",
            "description": "This category encompasses various engineering disciplines such as electrical engineering, mechanical engineering, and software engineering."
        },
        {
            "name": "Social Sciences",
            "sub_class": None,
            "model": None,
            "type": "Academic",
            "description": "Social sciences cover fields such as economics, sociology, psychology, and political sciences."
        },
        {
            "name": "Natural Sciences",
            "sub_class": None,
            "model": None,
            "type": "Academic",
            "description": "Natural sciences comprise subjects like physics, chemistry, biology, and geology."
        },
        {
            "name": "Humanities",
            "sub_class": None,
            "model": None,
            "type": "Academic",
            "description": "Humanities encompass disciplines like literature, visual arts, music, and theater."
        },
    ]

    for field in fields:
        Classification.objects.create(
            name=field["name"],
            sub_class=field["sub_class"],
            model=field["model"],
            type=field["type"],
            description=field["description"]
        )


def translateImport12():
    fields = [
        {
            "name": "Computer Science",
            "classification_id": 2,
            "description": "The field of study related to computer science and information technology."
        },
        {
            "name": "Electrical Engineering",
            "classification_id": 2,
            "description": "The field of study related to electrical and electronic engineering."
        },
        {
            "name": "Medical Sciences",
            "classification_id": 4,
            "description": "The field of study related to medical sciences and health."
        },
        {
            "name": "Mechanical Engineering",
            "classification_id": 4,
            "description": "The field of study related to mechanical engineering and energy."
        },
        {
            "name": "Social Sciences",
            "classification_id": 3,
            "description": "The field of study related to social and human sciences."
        },
        {
            "name": "Business Management",
            "classification_id": 5,
            "description": "The field of study related to management and business."
        },
    ]

    for field in fields:
        FieldOfStudy.objects.create(
            name=field["name"],
            classification_id=field["classification_id"],
            description=field["description"]
        )


def specialtyImport1():
    specialties = [
        {
            'name': 'Allergy and Immunology',
            'abbreviation': 'AI',
            'description': 'Allergy and immunology specialists diagnose and treat allergies, asthma, and disorders related to the immune system.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Anesthesiology',
            'abbreviation': 'Anes',
            'description': 'Anesthesiologists administer anesthesia during surgical procedures to ensure patient comfort and safety.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Dermatology',
            'abbreviation': 'Derm',
            'description': 'Dermatologists diagnose and treat skin conditions, including dermatitis, psoriasis, and skin cancer.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Diagnostic Radiology',
            'abbreviation': 'Rad',
            'description': 'Diagnostic radiologists use medical imaging techniques to diagnose and monitor various medical conditions.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Emergency Medicine',
            'abbreviation': 'EM',
            'description': 'Emergency medicine physicians handle acute medical conditions and emergencies in hospital emergency departments.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Family Medicine',
            'abbreviation': 'FM',
            'description': 'Family medicine practitioners provide primary care services to individuals and families of all ages.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Internal Medicine',
            'abbreviation': 'IM',
            'description': 'Internists focus on the prevention, diagnosis, and non-surgical treatment of adult diseases.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Medical Genetics',
            'abbreviation': 'Med Gen',
            'description': 'Medical geneticists study genetic disorders and provide genetic counseling and testing services.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Neurology',
            'abbreviation': 'Neurol',
            'description': 'Neurologists specialize in the diagnosis and treatment of disorders of the nervous system.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Nuclear Medicine',
            'abbreviation': 'Nucl Med',
            'description': 'Nuclear medicine physicians use radioactive substances for diagnostic and therapeutic purposes.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Doctor of Osteopathic Medicine',
            'abbreviation': 'DO',
            'description': 'A medical degree that qualifies individuals to become doctors of osteopathic medicine, emphasizing a holistic approach to patient care.',
            'degree_name': 'Doctor of Osteopathic Medicine',
            'is_active': False,
        },
    ]

    for specialty_data in specialties:
        degree_name = specialty_data.pop('degree_name')
        degree = EducationalDegree.objects.get(name=degree_name)
        Specialty.objects.create(degree=degree, **specialty_data)


def specialtyImport2():
    specialties = [
        {
            'name': 'Obstetrics and Gynecology',
            'abbreviation': 'OB/GYN',
            'description': 'Obstetricians and gynecologists provide healthcare services related to pregnancy, childbirth, and women\'s reproductive health.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Ophthalmology',
            'abbreviation': 'Ophth',
            'description': 'Ophthalmologists specialize in eye care, including diagnosing and treating eye diseases and performing eye surgeries.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pathology',
            'abbreviation': 'Path',
            'description': 'Pathologists study diseases through examination of tissues, cells, and bodily fluids to aid in diagnosis and treatment.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatrics',
            'abbreviation': 'Peds',
            'description': 'Pediatricians focus on the healthcare of infants, children, and adolescents, addressing their unique medical needs.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Physical Medicine and Rehabilitation',
            'abbreviation': 'PM&R',
            'description': 'Physiatrists specialize in physical medicine and rehabilitation, helping patients recover from injuries and improve their function.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Preventive Medicine',
            'abbreviation': 'Prev Med',
            'description': 'Preventive medicine specialists focus on disease prevention, health promotion, and community health.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Psychiatry',
            'abbreviation': 'Psych',
            'description': 'Psychiatrists diagnose and treat mental illnesses and emotional disorders, offering therapy and medication management.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Radiation Oncology',
            'abbreviation': 'Rad Onc',
            'description': 'Radiation oncologists use radiation therapy to treat cancer and manage its side effects.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Surgery',
            'abbreviation': 'Surg',
            'description': 'Surgeons perform surgical procedures to treat injuries, diseases, and conditions, often specializing in specific areas like cardiothoracic surgery or orthopedic surgery.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Urology',
            'abbreviation': 'Urol',
            'description': 'Urologists specialize in the diagnosis and treatment of conditions affecting the urinary tract and male reproductive system.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
    ]

    for specialty_data in specialties:
        degree_name = specialty_data.pop('degree_name')
        degree = EducationalDegree.objects.get(name=degree_name)
        Specialty.objects.create(degree=degree, **specialty_data)


def specialtyImport3():
    specialties = [
        {
            'name': 'Adult Gastroenterology',
            'abbreviation': 'GI',
            'description': 'Adult gastroenterologists diagnose and treat disorders of the digestive system, including the stomach, intestines, and liver.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Gastroenterology',
            'abbreviation': 'Ped GI',
            'description': 'Pediatric gastroenterologists specialize in digestive issues in children and adolescents.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult Pulmonology',
            'abbreviation': 'Pulm',
            'description': 'Adult pulmonologists diagnose and treat respiratory diseases and conditions in adults.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Pulmonology',
            'abbreviation': 'Ped Pulm',
            'description': 'Pediatric pulmonologists focus on respiratory issues in children and adolescents.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult Endocrinology',
            'abbreviation': 'Endo',
            'description': 'Adult endocrinologists specialize in hormonal disorders and diseases, such as diabetes and thyroid disorders.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Endocrinology',
            'abbreviation': 'Ped Endo',
            'description': 'Pediatric endocrinologists address hormonal issues in children and adolescents.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult Infectious Disease',
            'abbreviation': 'Infect Dis',
            'description': 'Infectious disease specialists diagnose and treat infections caused by bacteria, viruses, and other pathogens.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Infectious Disease',
            'abbreviation': 'Ped Infect Dis',
            'description': 'Pediatric infectious disease specialists focus on infectious diseases in children.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult Rheumatology',
            'abbreviation': 'Rheum',
            'description': 'Adult rheumatologists diagnose and treat autoimmune and musculoskeletal disorders.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Rheumatology',
            'abbreviation': 'Ped Rheum',
            'description': 'Pediatric rheumatologists specialize in autoimmune and musculoskeletal conditions in children.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
    ]

    for specialty_data in specialties:
        degree_name = specialty_data.pop('degree_name')
        degree = EducationalDegree.objects.get(name=degree_name)
        Specialty.objects.create(degree=degree, **specialty_data)

def specialtyImport4():
    specialties = [
        {
            'name': 'Adult Nephrology',
            'abbreviation': 'Nephro',
            'description': 'Adult nephrologists specialize in the diagnosis and treatment of kidney diseases and disorders.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Nephrology',
            'abbreviation': 'Ped Nephro',
            'description': 'Pediatric nephrologists focus on kidney-related issues in children and adolescents.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult Hematology',
            'abbreviation': 'Hematol',
            'description': 'Adult hematologists diagnose and treat blood disorders, including anemia and leukemia.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Hematology',
            'abbreviation': 'Ped Hematol',
            'description': 'Pediatric hematologists specialize in blood disorders in children and adolescents.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult Orthopedics',
            'abbreviation': 'Ortho',
            'description': 'Adult orthopedic surgeons diagnose and treat musculoskeletal conditions and perform orthopedic surgeries.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Orthopedics',
            'abbreviation': 'Ped Ortho',
            'description': 'Pediatric orthopedic surgeons specialize in musculoskeletal issues in children and adolescents.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult Otolaryngology',
            'abbreviation': 'Otolaryngol',
            'description': 'Adult otolaryngologists diagnose and treat ear, nose, and throat disorders.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Otolaryngology',
            'abbreviation': 'Ped Otolaryngol',
            'description': 'Pediatric otolaryngologists focus on ear, nose, and throat issues in children and adolescents.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult General Surgery',
            'abbreviation': 'Gen Surg',
            'description': 'Adult general surgeons perform a wide range of surgical procedures on adults.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric General Surgery',
            'abbreviation': 'Ped Gen Surg',
            'description': 'Pediatric general surgeons specialize in surgical procedures for children and adolescents.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
    ]

    for specialty_data in specialties:
        degree_name = specialty_data.pop('degree_name')
        degree = EducationalDegree.objects.get(name=degree_name)
        Specialty.objects.create(degree=degree, **specialty_data)

def specialtyImport5():
    specialties = [
        {
            'name': 'Adult Plastic Surgery',
            'abbreviation': 'Plast Surg',
            'description': 'Adult plastic surgeons perform cosmetic and reconstructive surgery to enhance or restore appearance.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Plastic Surgery',
            'abbreviation': 'Ped Plast Surg',
            'description': 'Pediatric plastic surgeons specialize in cosmetic and reconstructive surgery for children.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult Cardiovascular Surgery',
            'abbreviation': 'Cardio Surg',
            'description': 'Adult cardiovascular surgeons perform surgeries on the heart and blood vessels in adults.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Cardiovascular Surgery',
            'abbreviation': 'Ped Cardio Surg',
            'description': 'Pediatric cardiovascular surgeons specialize in heart and vascular surgeries for children.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult Neurosurgery',
            'abbreviation': 'Neurosurg',
            'description': 'Adult neurosurgeons perform surgeries on the brain and nervous system in adults.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Neurosurgery',
            'abbreviation': 'Ped Neurosurg',
            'description': 'Pediatric neurosurgeons specialize in brain and nervous system surgeries for children.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Adult Oncology',
            'abbreviation': 'Oncol',
            'description': 'Adult oncologists diagnose and treat cancer in adults, often specializing in specific types of cancer.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Pediatric Oncology',
            'abbreviation': 'Ped Oncol',
            'description': 'Pediatric oncologists specialize in the treatment of cancer in children and adolescents.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Breast Surgery',
            'abbreviation': 'Breast Surg',
            'description': 'Breast surgeons perform surgeries related to breast health, including cancer treatment.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Thoracic Surgery',
            'abbreviation': 'Thorac Surg',
            'description': 'Thoracic surgeons specialize in surgeries involving the chest and thoracic organs.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
    ]

    for specialty_data in specialties:
        degree_name = specialty_data.pop('degree_name')
        degree = EducationalDegree.objects.get(name=degree_name)
        Specialty.objects.create(degree=degree, **specialty_data)

def specialtyImport6():
    specialties = [
        {
            'name': 'Hand Surgery',
            'abbreviation': 'Hand Surg',
            'description': 'Hand surgeons specialize in the diagnosis and treatment of hand and upper extremity conditions.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Facial Plastic Surgery',
            'abbreviation': 'Facial Plast Surg',
            'description': 'Facial plastic surgeons perform surgeries to enhance or reconstruct the face and neck.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Colorectal Surgery',
            'abbreviation': 'Colorectal Surg',
            'description': 'Colorectal surgeons specialize in the treatment of disorders affecting the colon, rectum, and anus.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Head and Neck Surgery',
            'abbreviation': 'Head Neck Surg',
            'description': 'Head and neck surgeons diagnose and treat conditions in the head, neck, and throat.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Vascular Surgery',
            'abbreviation': 'Vasc Surg',
            'description': 'Vascular surgeons perform surgeries on blood vessels and arteries to treat vascular conditions.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Hand Nerve Surgery',
            'abbreviation': 'Hand Nerve Surg',
            'description': 'Hand nerve surgeons specialize in treating nerve-related issues in the hand and upper extremities.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Burn Surgery',
            'abbreviation': 'Burn Surg',
            'description': 'Burn surgeons treat burn injuries and help with the healing and reconstruction process.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Reconstructive Plastic Surgery',
            'abbreviation': 'Recon Plast Surg',
            'description': 'Reconstructive plastic surgeons focus on restoring form and function after injuries or surgeries.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Cosmetic Plastic Surgery',
            'abbreviation': 'Cosmetic Plast Surg',
            'description': 'Cosmetic plastic surgeons perform surgeries to enhance a person\'s appearance.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Body Contouring Surgery',
            'abbreviation': 'Body Contour Surg',
            'description': 'Body contouring surgeons reshape and sculpt the body through surgical procedures.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
    ]

    for specialty_data in specialties:
        degree_name = specialty_data.pop('degree_name')
        degree = EducationalDegree.objects.get(name=degree_name)
        Specialty.objects.create(degree=degree, **specialty_data)

def specialtyImport7():
    specialties = [
        {
            'name': 'Craniofacial Surgery',
            'abbreviation': 'Craniofacial Plast Surg',
            'description': 'Craniofacial plastic surgeons specialize in surgeries involving the skull and face.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Hand Plastic Surgery',
            'abbreviation': 'Hand Plast Surg',
            'description': 'Hand plastic surgeons perform cosmetic and reconstructive procedures on the hand.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Dermatologic Surgery',
            'abbreviation': 'Derm Surg',
            'description': 'Dermatologic surgeons specialize in surgical procedures related to the skin.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Lower Extremity Plastic Surgery',
            'abbreviation': 'Lower Extrem Plast Surg',
            'description': 'Lower extremity plastic surgeons focus on procedures involving the legs and feet.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Upper Extremity Plastic Surgery',
            'abbreviation': 'Upper Extrem Plast Surg',
            'description': 'Upper extremity plastic surgeons specialize in procedures related to the arms and hands.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Respiratory Plastic Surgery',
            'abbreviation': 'Resp Plast Surg',
            'description': 'Respiratory plastic surgeons focus on procedures related to the respiratory system.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Gastrointestinal Plastic Surgery',
            'abbreviation': 'GI Plast Surg',
            'description': 'Gastrointestinal plastic surgeons specialize in procedures involving the digestive tract.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Urogenital Plastic Surgery',
            'abbreviation': 'Urogen Plast Surg',
            'description': 'Urogenital plastic surgeons focus on procedures related to the urinary and genital systems.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Neurological Plastic Surgery',
            'abbreviation': 'Neurol Plast Surg',
            'description': 'Neurological plastic surgeons specialize in procedures involving the nervous system.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
        {
            'name': 'Oncologic Plastic Surgery',
            'abbreviation': 'Oncol Plast Surg',
            'description': 'Oncologic plastic surgeons focus on procedures related to cancer treatment and reconstruction.',
            'degree_name': 'Doctor of Medicine',
            'is_active': False,
        },
    ]

    for specialty_data in specialties:
        degree_name = specialty_data.pop('degree_name')
        degree = EducationalDegree.objects.get(name=degree_name)
        Specialty.objects.create(degree=degree, **specialty_data)

def specialtyImport8():
    specialties = [
        # {
        #     'name': 'Breast Reconstruction Surgery',
        #     'abbreviation': 'Breast Recon Plast Surg',
        #     'description': 'Breast reconstruction surgeons restore the breast after cancer surgery or injury.',
        #     'degree_name': 'Doctor of Medicine',
        #     'is_active': False,
        # },
        # {
        #     'name': 'Breast Cosmetic Surgery',
        #     'abbreviation': 'Breast Cosmetic Plast Surg',
        #     'description': 'Breast cosmetic surgeons enhance the appearance of the breast.',
        #     'degree_name': 'Doctor of Medicine',
        #     'is_active': False,
        # },
        # {
        #     'name': 'Breast Body Contouring Surgery',
        #     'abbreviation': 'Breast Body Contour Plast Surg',
        #     'description': 'Breast body contouring surgeons reshape the breast area.',
        #     'degree_name': 'Doctor of Medicine',
        #     'is_active': False,
        # },
        # {
        #     'name': 'Breast Craniofacial Surgery',
        #     'abbreviation': 'Breast Craniofacial Plast Surg',
        #     'description': 'Breast craniofacial surgeons specialize in procedures involving the breast, skull, and face.',
        #     'degree_name': 'Doctor of Medicine',
        #     'is_active': False,
        # },
        # {
        #     'name': 'Sleep Medicine',
        #     'abbreviation': 'Sleep Med',
        #     'description': 'Sleep medicine specialists diagnose and treat sleep disorders, such as sleep apnea.',
        #     'degree_name': 'Doctor of Medicine',
        #     'is_active': False,
        # },
        # {
        #     'name': 'Sports Medicine',
        #     'abbreviation': 'Sports Med',
        #     'description': 'Sports medicine specialists focus on the treatment and prevention of sports-related injuries.',
        #     'degree_name': 'Doctor of Medicine',
        #     'is_active': False,
        # },
        {
            'name': 'Massage Therapist',
            'abbreviation': 'Massage Therapist',
            'description': 'Massage therapists provide therapeutic massages to promote relaxation and alleviate pain.',
            'degree_name': 'Certificate or Diploma in Massage Therapy',
            'is_active': False,
        },
        {
            'name': 'Nutrition Consultant',
            'abbreviation': 'Nutr Consultant',
            'description': 'Nutrition consultants provide dietary advice and guidance to promote healthy eating habits.',
            'degree_name': "Bachelor's degree in Nutrition or related field",
            'is_active': False,
        },
        {
            'name': 'Healthcare Social Worker',
            'abbreviation': 'HC Social Worker',
            'description': 'Healthcare social workers support patients and families in dealing with healthcare challenges.',
            'degree_name': "Master's degree in Social Work (MSW)",
            'is_active': False,
        },
        {
            'name': 'Fitness Trainer',
            'abbreviation': 'Fitness Trainer',
            'description': 'Fitness trainers design exercise programs and provide guidance to help clients achieve fitness goals.',
            'degree_name': 'Certification in Fitness Training',
            'is_active': False,
        },
    ]

    for specialty_data in specialties:
        degree_name = specialty_data.pop('degree_name')
        degree = EducationalDegree.objects.get(name=degree_name)
        Specialty.objects.create(degree=degree, **specialty_data)

def degree01():
    # Certificate or Diploma in Massage Therapy
    # EducationalDegree.objects.create(
    #     name="Certificate or Diploma in Massage Therapy",
    #     abbreviation="Cert/Diploma Massage",
    #     description="Certificate or Diploma in Massage Therapy",
    #     duration_years=2,  # Adjust the duration as needed
    # )

    # # Bachelor's degree in Nutrition or related field
    # EducationalDegree.objects.create(
    #     name="Bachelor's degree in Nutrition or related field",
    #     abbreviation="Bachelors Nutrition",
    #     description="Bachelor's degree in Nutrition or related field",
    #     duration_years=4,  # Adjust the duration as needed
    # )

    # # Master's degree in Social Work (MSW)
    # EducationalDegree.objects.create(
    #     name="Master's degree in Social Work (MSW)",
    #     abbreviation="MSW",
    #     description="Master's degree in Social Work (MSW)",
    #     duration_years=2,  # Adjust the duration as needed
    # )

    # # Certification in Fitness Training
    # EducationalDegree.objects.create(
    #     name="Certification in Fitness Training",
    #     abbreviation="Cert Fitness",
    #     description="Certification in Fitness Training",
    #     duration_years=1,  # Adjust the duration as needed
    # )

    # # Master's degree in Psychology or related field
    # EducationalDegree.objects.create(
    #     name="Master's degree in Psychology or related field",
    #     abbreviation="MS Psychology",
    #     description="Master's degree in Psychology or related field",
    #     duration_years=2,  # Adjust the duration as needed
    # )

    # # Certification in Yoga or Mindfulness
    # EducationalDegree.objects.create(
    #     name="Certification in Yoga or Mindfulness",
    #     abbreviation="Cert Yoga/Mindfulness",
    #     description="Certification in Yoga or Mindfulness",
    #     duration_years=1,  # Adjust the duration as needed
    # )

    # # Certification in Breathing Exercises
    # EducationalDegree.objects.create(
    #     name="Certification in Breathing Exercises",
    #     abbreviation="Cert Breathing",
    #     description="Certification in Breathing Exercises",
    #     duration_years=1,  # Adjust the duration as needed
    # )

    # # Doctoral degree in Psychology (Ph.D. or Psy.D.)
    # EducationalDegree.objects.create(
    #     name="Doctoral degree in Psychology (Ph.D. or Psy.D.)",
    #     abbreviation="Ph.D./Psy.D. Psychology",
    #     description="Doctoral degree in Psychology (Ph.D. or Psy.D.)",
    #     duration_years=5,  # Adjust the duration as needed
    # )

    # # Bachelor's degree in Nutrition and Dietetics
    # EducationalDegree.objects.create(
    #     name="Bachelor's degree in Nutrition and Dietetics",
    #     abbreviation="Bachelors Nutrition/Dietetics",
    #     description="Bachelor's degree in Nutrition and Dietetics",
    #     duration_years=4,  # Adjust the duration as needed
    # )

    # # Associate's or Bachelor's degree in Dental Hygiene
    # EducationalDegree.objects.create(
    #     name="Associate's or Bachelor's degree in Dental Hygiene",
    #     abbreviation="Assoc/Bachelors Dental Hygiene",
    #     description="Associate's or Bachelor's degree in Dental Hygiene",
    #     duration_years=2,  # Adjust the duration as needed
    # )

    # # Bachelor's degree in Nutrition or related field
    # EducationalDegree.objects.create(
    #     name="Bachelor's degree in Nutrition or related field",
    #     abbreviation="Bachelors Nutrition/Related",
    #     description="Bachelor's degree in Nutrition or related field",
    #     duration_years=4,  # Adjust the duration as needed
    # )

    # Bachelor's degree in Medical Technology or related field
    EducationalDegree.objects.create(
        name="Bachelor's degree in Medical Technology or related field",
        abbreviation="Bachelors Med Tech/Related",
        description="Bachelor's degree in Medical Technology or related field",
        duration_years=4,  # Adjust the duration as needed
    )

    # Doctor of Medicine (MD) or Doctor of Osteopathic Medicine (DO)
    EducationalDegree.objects.create(
        name="Doctor of Medicine (MD) or Doctor of Osteopathic Medicine (DO)",
        abbreviation="MD/DO",
        description="Doctor of Medicine (MD) or Doctor of Osteopathic Medicine (DO)",
        duration_years=4,  # Adjust the duration as needed
    )

def specialtyImport9():
    specialties = [
        # {
        #     'name': 'Behavioral Therapy Specialist',
        #     'abbreviation': 'Behav Therapist',
        #     'description': 'Behavioral therapy specialists use therapeutic techniques to address behavioral and emotional issues.',
        #     'degree_name': "Master's degree in Psychology or related field",
        #     'is_active': False,
        # },
        # {
        #     'name': 'Yoga and Mindfulness Specialist',
        #     'abbreviation': 'Yoga/Mindfulness Spec',
        #     'description': 'Yoga and mindfulness specialists promote mental and emotional well-being through practices like yoga and meditation.',
        #     'degree_name': 'Certification in Yoga or Mindfulness',
        #     'is_active': False,
        # },
        # {
        #     'name': 'Breathing Exercise Specialist',
        #     'abbreviation': 'Breath Exercise Spec',
        #     'description': 'Breathing exercise specialists teach techniques to improve respiratory health and well-being.',
        #     'degree_name': 'Certification in Breathing Exercises',
        #     'is_active': False,
        # },
        # {
        #     'name': 'Health Psychology Specialist',
        #     'abbreviation': 'Health Psychologist',
        #     'description': 'Health psychology specialists focus on the psychological aspects of health and illness.',
        #     'degree_name': 'Doctoral degree in Psychology (Ph.D. or Psy.D.)',
        #     'is_active': False,
        # },
        # {
        #     'name': 'Dental Hygiene Specialist',
        #     'abbreviation': 'Dental Hygiene Spec',
        #     'description': 'Dental hygiene specialists promote oral health through preventive care and education.',
        #     'degree_name': "Associate's or Bachelor's degree in Dental Hygiene",
        #     'is_active': False,
        # },
        # {
        #     'name': 'Nutrition and Dietetics Specialist',
        #     'abbreviation': 'Nutr Dietetics Spec',
        #     'description': 'Nutrition and dietetics specialists provide expert dietary advice and guidance.',
        #     'degree_name': "Bachelor's degree in Nutrition and Dietetics",
        #     'is_active': False,
        # },
        # {
        #     'name': 'Nutrition Consultant',
        #     'abbreviation': 'Nutr Consultant',
        #     'description': 'Nutrition consultants provide dietary advice and guidance to promote healthy eating habits.',
        #     'degree_name': "Bachelor's degree in Nutrition or related field",
        #     'is_active': False,
        # },
        {
            'name': 'Medical Technology',
            'abbreviation': 'Med Tech',
            'description': 'Medical technologists perform laboratory tests and operate medical equipment.',
            'degree_name': "Bachelor's degree in Medical Technology or related field",
            'is_active': False,
        },
        {
            'name': 'Telemedicine',
            'abbreviation': 'Telemedicine',
            'description': 'Telemedicine involves providing medical services remotely, often through digital communication.',
            'degree_name': 'Doctor of Medicine (MD) or Doctor of Osteopathic Medicine (DO)',
            'is_active': False,
        },
        {
            'name': 'Aerospace Medicine',
            'abbreviation': 'Aero Med',
            'description': 'Aerospace medicine specialists focus on the health and well-being of individuals in the aerospace industry.',
            'degree_name': 'Doctor of Medicine (MD) or Doctor of Osteopathic Medicine (DO)',
            'is_active': False,
        },
    ]

    for specialty_data in specialties:
        degree_name = specialty_data.pop('degree_name')
        degree = EducationalDegree.objects.get(name=degree_name)
        Specialty.objects.create(degree=degree, **specialty_data)

def create_classifications_for_procedures():
    classifications = [
        {
            'name': 'Cosmetic Plastic Surgery',
            'type': 'Medical Procedure Classification',
            'description': 'Procedures related to cosmetic plastic surgery for facial rejuvenation',
        },
        {
            'name': 'Cosmetic Plastic Surgery',
            'sub_class': 'Facial Rejuvenation',
            'type': 'Medical Procedure Classification',
            'description': 'Procedures for facial rejuvenation within the field of cosmetic plastic surgery',
        },
        {
            'name': 'Cosmetic Plastic Surgery',
            'sub_class': 'Non-Surgical Facial Rejuvenation',
            'type': 'Medical Procedure Classification',
            'description': 'Non-surgical procedures for facial rejuvenation within the field of cosmetic plastic surgery',
        },
    ]

    for classification_data in classifications:
        Classification.objects.create(**classification_data)


def procedureImport():
    procedures = [
        {
            'name': 'Nose Job',
            'code': 1,
            'description': 'Surgical procedure to improve the shape of the nose',
            'skills': 'Plastic surgery',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
        {
            'name': 'Facelift Surgical Facial Rejuvenation',
            'code': 2,
            'description': 'Surgical facelift procedure to rejuvenate the face',
            'skills': 'Plastic surgery, facial surgery',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
        {
            'name': 'Blepharoplasty Surgical Facial Rejuvenation',
            'code': 3,
            'description': 'Eyelid lift surgical procedure',
            'skills': 'Plastic surgery, eyelid surgery',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
        {
            'name': 'Canthoplasty Surgical Facial Rejuvenation',
            'code': 4,
            'description': 'Canthoplasty surgical procedure',
            'skills': 'Plastic surgery, canthoplasty',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
        {
            'name': 'Otoplasty Surgical Facial Rejuvenation',
            'code': 5,
            'description': 'Surgical procedure to improve the shape of the ears',
            'skills': 'Plastic surgery, ear surgery',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
        {
            'name': 'Buccal Fat Removal Surgical Facial Rejuvenation',
            'code': 6,
            'description': 'Surgical procedure to remove buccal fat',
            'skills': 'Plastic surgery, buccal fat removal',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
        {
            'name': 'Thread Lift Surgical Facial Rejuvenation',
            'code': 7,
            'description': 'Surgical thread lift procedure for the face',
            'skills': 'Plastic surgery, facial thread lift',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
        {
            'name': 'Dermal Filler Non Surgical Facial Rejuvenation',
            'code': 8,
            'description': 'Non-surgical dermal filler procedure for the face',
            'skills': 'Facial dermal filler injection',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Non-Surgical Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
        {
            'name': 'Ultherapy Non Surgical Facial Rejuvenation',
            'code': 9,
            'description': 'Non-surgical Ultherapy procedure for facial rejuvenation',
            'skills': 'Ultherapy for the face',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Non-Surgical Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
        {
            'name': 'HIFU Non Surgical Facial Rejuvenation',
            'code': 10,
            'description': 'Non-surgical HIFU procedure for facial rejuvenation',
            'skills': 'HIFU for the face',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Non-Surgical Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
        {
            'name': 'Chemical Peel Non Surgical Facial Rejuvenation',
            'code': 11,
            'description': 'Non-surgical chemical peel procedure for the face',
            'skills': 'Facial chemical peel',
            'cost_id': 1,
            'classification_data': {
                'name': 'Cosmetic Plastic Surgery',
                'sub_class': 'Non-Surgical Facial Rejuvenation',
                'type': 'Medical Procedure Classification',
            },
        },
    ]

    for procedure_data in procedures:
        classification_data = procedure_data.pop('classification_data')
        cost_id = procedure_data.pop('cost_id')

        # یافتن یا ایجاد Classification
        classification, created = Classification.objects.get_or_create(**classification_data)

        # یافتن Cost
        cost = Cost.objects.get(id=cost_id)

        # ایجاد Procedure
        procedure = Procedure(cost=cost, **procedure_data)
        procedure.save()

        # اضافه کردن Classification به Procedure
        procedure.classification.add(classification)



# def specialtyImport():
#     specialties = [
#     ]

#     for specialty_data in specialties:
#         degree_name = specialty_data.pop('degree_name')
#         degree = EducationalDegree.objects.get(name=degree_name)
#         Specialty.objects.create(degree=degree, **specialty_data)



context_procedures = [
    {
        'name': 'Packages',
        'sub_categories': [
            {
                'name': 'Cosmetic',
                'sub_categories': [
                    {
                        'name': 'Nose Job',
                        'sub_categories': []
                    },
                    {
                        'name': 'Facial Rejuvenation',
                        'sub_categories': [
                            {
                                'name': 'Surgical',
                                'sub_categories': [
                                    {'name': 'Facelift', 'sub_categories': []},
                                    {'name': 'Blepharoplasty', 'sub_categories': []},
                                    {'name': 'Canthoplasty', 'sub_categories': []},
                                    {'name': 'Otoplasty', 'sub_categories': []},
                                    {'name': 'Buccal Fat Removal', 'sub_categories': []},
                                    {'name': 'Thread Lift', 'sub_categories': []},
                                ]
                            },
                            {
                                'name': 'Non Surgical',
                                'sub_categories': [
                                    {'name': 'Dermal Filler', 'sub_categories': []},
                                    {'name': 'Ultherapy', 'sub_categories': []},
                                    {'name': 'HIFU', 'sub_categories': []},
                                    {'name': 'Chemical Peel', 'sub_categories': []},
                                ]
                            },
                        ]
                    },
                    {
                        'name': 'Body Contouring',
                        'sub_categories': [
                            {
                                'name': 'Surgical',
                                'sub_categories': [
                                    {'name': 'Mommy Makeover', 'sub_categories': []},
                                    {'name': 'Lower Body Lift', 'sub_categories': []},
                                    {'name': 'Upper Body Lift', 'sub_categories': []},
                                    {'name': 'Brachioplasty', 'sub_categories': []},
                                    {'name': 'Tummy tuck', 'sub_categories': []},
                                    {'name': 'Liposuction', 'sub_categories': []},
                                ]
                            },
                            {
                                'name': 'Non Surgical',
                                'sub_categories': [
                                    {'name': 'CoolSculpting In Iran', 'sub_categories': []},
                                ]
                            },
                        ]
                    },
                    {
                        'name': 'Vaginal Rejuvenation',
                        'sub_categories': [
                            {'name': 'Labiaplasty', 'sub_categories': []},
                            {'name': 'Vaginoplasty', 'sub_categories': []},
                        ]
                    },
                    {
                        'name': 'Breast',
                        'sub_categories': [
                            {'name': 'Breast Reduction', 'sub_categories': []},
                            {'name': 'Breast Lift', 'sub_categories': []},
                            {'name': 'Breast Augmentation', 'sub_categories': []},
                        ]
                    },
                    {
                        'name': 'Buttock',
                        'sub_categories': [
                            {'name': 'Brazilian Butt Lift', 'sub_categories': []},
                            {'name': 'Butt Implants', 'sub_categories': []},
                        ]
                    },
                    {
                        'name': 'Dental',
                        'sub_categories': [
                            {'name': 'Dental Implant', 'sub_categories': []},
                            {'name': 'Hollywood Smile', 'sub_categories': []},
                        ]
                    },
                    {
                        'name': 'Bariatric',
                        'sub_categories': [
                            {'name': 'Gastric Sleeve', 'sub_categories': []},
                            {'name': 'Roux-en-Y Gastric Bypass', 'sub_categories': []},
                        ]
                    },
                    {'name': 'Hair Transplant', 'sub_categories': []},
                ]
            },
            {
                'name': 'Reconstructive & Medical',
                'sub_categories': [
                    {
                        'name': 'Dental Treatment',
                        'sub_categories': []
                    },
                    {
                        'name': 'Fertility Treatments',
                        'sub_categories': [
                            {'name': 'IVF', 'sub_categories': []},
                            {'name': 'IUI', 'sub_categories': []},
                        ]
                    },
                    {'name': 'Kidney Transplant', 'sub_categories': []},
                    {
                        'name': 'ENT Surgery',
                        'sub_categories': [
                            {'name': 'Head and Neck Surgery', 'sub_categories': []},
                            {'name': 'Throat Surgery', 'sub_categories': []},
                            {'name': 'Ear Surgery', 'sub_categories': []},
                            {'name': 'Rhinology Surgery', 'sub_categories': []},
                        ]
                    },
                ]
            },
        ]
    },
    {
        'name': 'Services',
        'index': 1,
        'sub_categories': [
            {
                'name': 'General Services',
                'index': 1,
                'sub_categories': []
            },
            {
                'name': 'Medical Check ups',
                'index': 1,
                'sub_categories': []
            },
            {
                'name': 'Amazing Tours',
                'index': 1,
                'sub_categories': []
            },
            {
                'name': 'Iranian Delicious Food',
                'index': 1,
                'sub_categories': []
            },
            {
                'name': 'Unique Souvenirs',
                'index': 1,
                'sub_categories': []
            },
        ]
    }
]



def create_menus(categories, parent=None):
    for category_data in categories:
        name = category_data['name']
        ind = category_data['index'] if 'index' in category_data else 0
        menu = SettingMenus(index=ind, name=name, parent=parent)
        menu.save()
        if 'sub_categories' in category_data:
            create_menus(category_data['sub_categories'], parent=menu)

