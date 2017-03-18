from .models import Programa

def if_in_sigpae(codigo,trimestre,anio):
	query = Programa.objects.filter(codigo=codigo,fecha_vigAno=anio,fecha_vigTrim=trimestre).order_by('fecha_vigAno','fecha_vigTrim')
	return len(query) > 0


def queries_sigpae(codigo,trimestre,anio):
    # Consulta para tratar de hallar el programa vigente para un trimestre.
	trimestre_none = (trimestre=="" or trimestre is None)
	anio_none = (anio=="" or anio is None)

    list_code = Programa.objects.filter(codigo=codigo)


    if(trimestre_none and anio_none):
	    return list_code.order_by('-fecha_vigAno','-fecha_vigTrim')

    elif(not trimestre_none and anio_none):
	    return list_code.filter(fecha_vigTrim__lte=trimestre).order_by('-fecha_vigAno','-fecha_vigTrim')

    elif(trimestre_none and not anio_none):
	    return list_code.filter(fecha_vigAno__lte=anio).order_by('-fecha_vigAno','-fecha_vigTrim')	

    else:
	    return list_code.filter(fecha_vigAno__lte=anio,fecha_vigTrim__lte=trimestre).order_by('-fecha_vigAno','-fecha_vigTrim')
