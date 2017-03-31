from django.core.management.base import BaseCommand
from django.db import models
from pdfapp.models import Author, Reference, Program, Code

class Command(BaseCommand):
    help="Insert test assignatures"
    def handle(self, *args, **options):
        print("If, somehow, you need to test something with a transcription but:")
        print(" a) You don't have OCRopy.")
        print(" b) Someone broke the transcriptions.")
        print(" c) For whatever reason you have to test a field that is not implemented yet.")
        print("Then you can use this. Want to DELETE (D) or CREATE(C)?", end="")
        ans = input()
        if (ans.lower() == "d"):
            print("Deleting")
            Reference.objects.filter(title="Author's book").delete()
            Reference.objects.filter(title="Whyyyy").delete()
            Program.objects.filter(document=None).delete()
            Author.objects.filter(first_surname="Plusone").delete()
            Author.objects.filter(first_surname="Sneaky").delete()
            Author.objects.filter(first_surname="Meteos").delete()
            print("Done.")
        elif (ans.lower() == "c"):
            print("Creating. Be sure to call this again to delete.")

            a1 = Author.objects.create(
                first_name="Author",
                first_surname="Plusone",
            )

            a2 = Author.objects.create(
                first_name="Zacharias",
                first_surname="Sneaky",
            )

            a3 = Author.objects.create(
                first_name="Dark",
                first_surname="Meteos",
            )

            r1 = Reference.objects.create(
                title="Author's book",
            )
            r1.author.add(a1)

            r2 = Reference.objects.create(
                title="Whyyyy",
            )
            r2.author.add(a2,a3)

            print("Number = 2505.")
            p1 = Program.objects.create(
                code = Code.objects.filter(code="CI").get(),
                number="2505",
                validity_year="1996",
                validity_trimester="1Abr-Jul",
            )
            p1.recommended_sources.add(r1,r2)
            print("Done.")
        else:
            print("Non-valid option. Bye.")
