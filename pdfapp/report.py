from .models import Programa
from django.db.models import Q

def report(code,trimester,year):
    # Query to retrieve all programs or transcripts.
    Programa.objects.filter(codigo=codigo)
