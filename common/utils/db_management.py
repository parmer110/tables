import docx
import re
from django.core.management.base import BaseCommand
from common.models import Translate

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
