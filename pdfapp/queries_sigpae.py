from .models import Programa, Program, Code, Reference, Author
from django.db.models import Min

# Checks if a str variable is none or empty
def check_none(a):
    return (a=="" or a is None)

def if_in_sigpae(codigo,trimestre,anio):
    if check_none(codigo) or check_none(trimestre) or check_none(anio):
        return False
    query = Programa.objects.filter(codigo=codigo,fecha_vigAno=anio,fecha_vigTrim=trimestre).order_by('fecha_vigAno','fecha_vigTrim')
    return len(query) > 0


def queries_sigpae(codigo,trimestre,anio):
    # Consulta para tratar de hallar el programa vigente para un trimestre.
    trimestre_none = check_none(trimestre)
    anio_none = check_none(anio)

    list_code = Programa.objects.filter(codigo=codigo)


    if(trimestre_none and anio_none):
        return list_code.order_by('-fecha_vigAno','-fecha_vigTrim')

    elif(not trimestre_none and anio_none):
        return list_code.filter(fecha_vigTrim__lte=trimestre).order_by('-fecha_vigAno','-fecha_vigTrim')

    elif(trimestre_none and not anio_none):
        return list_code.filter(fecha_vigAno__lte=anio).order_by('-fecha_vigAno','-fecha_vigTrim')  

    else:
        return list_code.filter(fecha_vigAno__lte=anio,fecha_vigTrim__lte=trimestre).order_by('-fecha_vigAno','-fecha_vigTrim')

def report_transcriptions(code):
    # Return all transcriptions related to code.
    return Program.objects.filter(code__code=code).order_by('code__code','validity_year','validity_trimester')

def report_programs(code):
    # Return all programs related to code.
    if (len(code) == 3):
        list_codes = Programa.objects.filter(codigo__regex='^[a-zA-Z]{3}[0-9]{3}$')
    elif (len(code) == 2):
        list_codes = Programa.objects.filter(codigo__regex='^[a-zA-Z]{2}[0-9]{4}$')
    return list_codes.filter(codigo__istartswith=code).order_by('codigo','fecha_vigAno','fecha_vigTrim')


def report_refs(code,trimester,year):
    # Returns information sources for a code and a time period.
    list_programs = Program.objects.none()
    if check_none(code):
        list_programs = Program.objects.filter(validity_year__lte=year,
                                                validity_trimester__lte=trimester
                                                ).order_by('-validity_year',
                                                            '-validity_trimester'
                                                )
    else:
        list_programs = Program.objects.filter(code__code=code,
                                                validity_year__lte=year,
                                                validity_trimester__lte=trimester
                                                ).order_by('-validity_year',
                                                            '-validity_trimester'
                                                )
    list_refs = Reference.objects.none()
    for p in list_programs:
        list_refs = list_refs | p.recommended_sources    
    return list_refs.annotate(mini=Min('author__first_surname')).order_by('mini').distinct()
        
