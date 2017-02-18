"""
Command to delete everything
Made by Christian Oliveros ( oliveroschristian.wordpress.com)
Last edit 02/12/2017
"""
from django.core.management.base import BaseCommand
from pdfapp.models import Document
from django.core.files.storage import default_storage
import sys

class Command(BaseCommand):
    help="Delete all the documents. Use with care"
    def handle(self, *args, **options):
        print("WARNING DELETING ALL THE DOCUMENTS", file=sys.stderr)
        print("Sure? (y/n): ", end="", file=sys.stderr)
        ans = input()
        if (ans == "y"):
            print("DELETING", file=sys.stderr)
            for doc in Document.objects.all():
                print("Deleting Document: " + doc.docfile.name)
                print("Saved in: " + doc.docfile.path)
                default_storage.delete(doc.docfile.path)
                doc.delete()
            print("Done")
        else:
            print("Nothing Deleted", file=sys.stderr)



        