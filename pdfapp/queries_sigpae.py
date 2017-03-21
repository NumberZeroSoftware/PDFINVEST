from .models import Programa

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
    trimestre_none = check_none(trimestre_none)
    anio_none = check_none(anio_none)

    list_code = Programa.objects.filter(codigo=codigo)


    if(trimestre_none and anio_none):
        return list_code.order_by('-fecha_vigAno','-fecha_vigTrim')

    elif(not trimestre_none and anio_none):
        return list_code.filter(fecha_vigTrim__lte=trimestre).order_by('-fecha_vigAno','-fecha_vigTrim')

    elif(trimestre_none and not anio_none):
        return list_code.filter(fecha_vigAno__lte=anio).order_by('-fecha_vigAno','-fecha_vigTrim')  

    else:
        return list_code.filter(fecha_vigAno__lte=anio,fecha_vigTrim__lte=trimestre).order_by('-fecha_vigAno','-fecha_vigTrim')
