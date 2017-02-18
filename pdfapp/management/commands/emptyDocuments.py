"""
Command to delete everything
Made by Christian Oliveros ( oliveroschristian.wordpress.com)
Last edit 02/12/2017
"""
from django.core.management.base import BaseCommand
from pdfapp.models import Document
from django.core.files.storage import default_storage
from django.conf import settings

from pathlib import Path
import shutil
import sys

class Command(BaseCommand):
    help="Delete all the documents. Use with care"
    def handle(self, *args, **options):
        print("WARNING DELETING ALL THE DOCUMENTS", file=sys.stderr)
        print("Sure? (y/n): ", end="", file=sys.stderr)
        ans = input()
        if (ans.lower() == "y"):
            print("DELETING", file=sys.stderr)
            for doc in Document.objects.all():
                print("Deleting Document: " + doc.docfile.name)
                print("Saved in: " + doc.docfile.path)
                default_storage.delete(doc.docfile.path)
                doc.delete()
            documents_folder = settings.MEDIA_ROOT+"/documents"
            print("Deleting Folder:", documents_folder)
            if Path(documents_folder).is_dir():
                shutil.rmtree(documents_folder, ignore_errors=False, onerror=None)
            print("Done")
        else:
            print("Nothing Deleted", file=sys.stderr)



        