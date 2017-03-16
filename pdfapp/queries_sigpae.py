from .models import Programa

def queries_sigpae(codigo,trimestre,anio):
	trimestre_none = (trimestre=="" or trimestre is None)
	anio_none = (anio=="" or anio is None)

	if(trimestre_none and anio_none):
		return Programa.objects.filter(codigo=codigo).order_by('fecha_vigAno','fecha_vigTrim')
	
	elif(not trimestre_none and anio_none):
		return Programa.objects.filter(codigo=codigo,fecha_vigTrim=trimestre).order_by('fecha_vigAno','fecha_vigTrim')
	
	elif(trimestre_none and not anio_none):
		return Programa.objects.filter(codigo=codigo,fecha_vigAno=anio).order_by('fecha_vigAno','fecha_vigTrim')	
	
	else:
		return Programa.objects.filter(codigo=codigo,fecha_vigAno=anio,fecha_vigTrim=trimestre).order_by('fecha_vigAno','fecha_vigTrim')
	
def if_in_sigpae(codigo,trimestre,anio):
	query = Programa.objects.filter(codigo=codigo,fecha_vigAno=anio,fecha_vigTrim=trimestre).order_by('fecha_vigAno','fecha_vigTrim')
	return len(query) > 0

