# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms import formset_factory, modelformset_factory

from .models import Document, Program, Department, Division, Code, Programa, AdditionalName, AdditionalField, Reference, Author
from .forms import UploadFileForm, ProgramForm, TextStringForm, DivErrorList, SigpaeSearchForm, AdditionalFieldForm, SigpaeReportForm, RefReportForm, ReferenceForm, ProgramReferenceForm
from .queries_sigpae import queries_sigpae, if_in_sigpae, report_transcriptions, report_programs, report_refs

from datetime import date
from pathlib import Path
import re, pdb
from pdb import set_trace

from utils.shell import call_main


def upload_view(request):
    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            # Lets get the filename and filepath
            tokens = re.match(r'((?P<filePath>([^\.])+)/)*(?P<fileName>[^\.\s/]+)\.pdf', newdoc.docfile.path)
            newdoc.file_name = tokens.group('fileName')
            newdoc.name = newdoc.file_name.upper()
            newdoc.file_path = tokens.group('filePath')
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('upload'))
        else:
            print('not valid')
    else:
        form = UploadFileForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'upload.html',
        {'documents': documents, 'form': form}
    )
    #Ver de que habria que hacer render entonces

# Get the edit view of a file
# request is the django request handle
# fileName is the name of the file without extension
# filePath is the file path of the pdf to edit
# TODO: better send file names rather than this
def edit_view(request, fileName, filePath=None,):
    render_dic = {}
    full_filePath = fileName
    if filePath is not None:
        full_filePath = filePath + "/" + fileName
    #Save fileName
    render_dic['fileName'] = fileName
    render_dic['filePath'] = filePath
    # Load documents to search for the requested file
    documents = Document.objects.all()
    html_file = None
    render_dic['html_string'] = 'File is being created. Please be patient.'
    try:
        doc = next(filter(lambda document: document.docfile.name == full_filePath+".pdf", documents))
        render_dic['doc'] = doc
        #Process file
        if not doc.ready_html and not doc.processing_html:
            doc.processing_html = True
            doc.ready_html = False
            doc.save()
        html_file = call_main(doc.file_path, doc.file_name) 
        
        if html_file is not None:
            possible_course_codes = Document.course_codes(html_file)
            course_dept_dict = {}
            for course_code in possible_course_codes:
                dept_code = course_code[0:3] if course_code[2].isalpha() else course_code[0:2]
                try:
                    course_dept_dict[course_code] = (dept_code, Code.objects.get(code=dept_code).department)
                    # if this succeded, then there are two options: 
                    #    department = None and department = some real department
                except Code.DoesNotExist:
                    course_dept_dict[course_code] = (dept_code, '')
                    # if this one is the case, then dept = ''
                    
            print(course_dept_dict)
            render_dic['course_dept_dict'] = course_dept_dict


    except StopIteration:
        render_dic['error'] = 'Error: File not found.'
        render_dic['html_string'] = 'Error: File not found.'
        return render(request, 'edit.html', render_dic)
    
    # Lets see if the html file is ready
    if html_file is not None:
        # We are still waiting for the textstring
        if doc.html_text_string is None:
            # Lets see if it really exists
            if Path(html_file).is_file():
                with open(html_file, 'r') as f:
                    doc.html_text_string = f.read()
                render_dic['html_string'] = doc.html_text_string
                doc.processing_html = False
                doc.ready_html = True
                doc.save()
            else:
                render_dic['html_string'] = 'File is being created. Please be patient.'
                render_dic['reload'] = True
                doc.ready_html = False
                doc.save()
        # We already got it
        else:
            render_dic['html_string'] = doc.html_text_string
            doc.processing_html = False
            doc.ready_html = True
            doc.save()
    else:
        render_dic['reload'] = True
        doc.ready_html = False
        doc.save()

    # Lets see if it is processing
    if 'reload' in render_dic:
        if Path(full_filePath).is_dir():
            doc.processing_html = True
            doc.save()
        else:
            doc.processing_html = False
            doc.save()
            call_main(doc.file_path, doc.file_name)
            doc.processing_html = True
            doc.save()

    print("---------------")
    print("Checking:", full_filePath+".pdf")
    print("Folder:", doc.file_path)
    print("Name:", doc.file_name)
    print("Processing:", doc.processing_html)
    print("Ready:", doc.ready_html)
    print("TextString on DB:", doc.html_text_string is not None)
    print("---------------")

    # Lets find the program information
    program, _ = Program.objects.get_or_create(document=doc)

    # Let get the additional fields
    initial_fields = []
    for extraField in program.additional_fields.all():
        initial_fields.append(
            {
            'pk' : extraField.pk, 
            'name': extraField.name,
            'new_name': "",
            'description' : extraField.description
            }
        )

    additionalFieldsFormset = formset_factory(AdditionalFieldForm, can_delete=True, extra=0)


    # # Let get the references
    # initial_refs = []
    # for ref in program.recommended_sources.all():
    #     initial_refs.append(
    #         {
    #         'reference' : extraField,
    #         }
    #     )

    #referenceFormset = formset_factory(ProgramReferenceForm, can_delete=True, extra=0)


    # Lets see if they are sending the information or requesting it
    if request.method == "POST": 
        program_form = ProgramForm(request.POST, instance=program, prefix="program", error_class=DivErrorList)
        textstring_form = TextStringForm(request.POST, instance=doc, prefix="textstring", error_class=DivErrorList)
        additionalFieldsForm = additionalFieldsFormset(request.POST, initial=initial_fields, error_class=DivErrorList)
        #referenceForm = referenceFormset(request.POST, initial=initial_refs, error_class=DivErrorList)

        if program_form.is_valid() and textstring_form.is_valid():
            program_form.save(commit=True)
            textstring_form.save(commit=True)
            # Lets Check If a something Changed
            if program_form.has_changed():
                if 'validity_date_m' in program_form.changed_data or 'validity_date_d' in program_form.changed_data \
                    or 'validity_date_y' in program_form.changed_data:
                    # Lets check we are not using null values
                    if program_form.cleaned_data['validity_date_y'] is not None \
                        and program_form.cleaned_data['validity_date_m'] is not None \
                        and program_form.cleaned_data['validity_date_d'] is not None:
                        program.validity_year = int(program_form.cleaned_data['validity_date_y'])
                        month = int(program_form.cleaned_data['validity_date_m'])
                        day = int(program_form.cleaned_data['validity_date_d'])
                        if month == 1:
                            program.validity_trimester = Program.TRIMESTER[0][0]
                        elif month == 2 or month == 3 or (month == 4 and day <= 15):
                            program.validity_trimester = Program.TRIMESTER[1][0]
                        elif (month == 4 and 15 < day) or (4 < month and month <= 9):
                            program.validity_trimester = Program.TRIMESTER[3][0]
                        elif 9 < month and month <= 12:
                            program.validity_trimester = Program.TRIMESTER[0][0]
                            program.validity_year += 1
                        program.save()

                # Lets put a fancy name
                if 'code' in program_form.changed_data or 'number' in program_form.changed_data \
                    or 'validity_year' in program_form.changed_data or 'validity_trimester' in program_form.changed_data:
                    if program_form.cleaned_data['code'] is not None \
                        and program_form.cleaned_data['number'] is not None:
                        doc.name = str(program_form.cleaned_data['code']).upper() + str(program_form.cleaned_data['number'])
                        if program_form.cleaned_data['validity_year'] is not None\
                        and program_form.cleaned_data['validity_trimester'] is not None:
                            doc.name = doc.name + '-' + str(program_form.cleaned_data['validity_year']).upper() \
                                + '-' + str(program.get_validity_trimester_display())
                        doc.save()

                # Check if it is already in SIGPAE
                if if_in_sigpae((str(program.code)+str(program.number)), program.validity_trimester, str(program.validity_year)):
                    render_dic['alert'] = "Advertencia: El Programa " + program.denomination + " " + str(program.code) + str(program.number) \
                        + " " + str(program.validity_year) + " " + program.get_validity_trimester_display() + " ya se encuentra en SIGPAE"

            for form in additionalFieldsForm.forms:
                if form.is_valid(): 
                    isPK = 'pk' in form.cleaned_data and (form.cleaned_data['pk'] is not None and form.cleaned_data['pk'] != "")
                    isName = 'name' in form.cleaned_data and (form.cleaned_data['name'] is not None and form.cleaned_data['name'] != "")
                    isNewName = 'new_name' in form.cleaned_data and (form.cleaned_data['new_name'] is not None and form.cleaned_data['new_name'] != "")
                    if 'DELETE' in form.cleaned_data and form.cleaned_data['DELETE'] and isPK :
                        print("Borrando", form.cleaned_data)
                        try:
                            AdditionalField.objects.get(pk=int(form.cleaned_data['pk'])).delete()
                        except Exception as e:
                            print (e)
                        
                        continue
                    elif 'name' not in form.cleaned_data or form.cleaned_data['name'] is None or form.cleaned_data['name'] == "":
                        print("Falta nombre en", form.cleaned_data)
                        form.add_error("name", "El Campo Nombre es Requerido") 
                        continue
                    elif isPK:
                        print("Ya lo conocia", form.cleaned_data)
                        obj = AdditionalField.objects.get(pk=int(form.cleaned_data['pk']))
                        if form.cleaned_data['name'] ==  AdditionalName.objects.get(name="Otro"):
                            if not isNewName:
                                form.add_error("new_name", "El Campo Nombre es Requerido") 
                                continue
                            real_name = AdditionalName.objects.get_or_create(name=form.cleaned_data['new_name'].title())[0]
                            real_name.save()
                        else:
                            real_name = form.cleaned_data['name']
                        obj.name = real_name
                        if 'description' in form.cleaned_data:
                            obj.description = form.cleaned_data['description']
                        else:
                            obj.description = ""
                        obj.save()
                    elif isName:
                        print("Nuevo", form.cleaned_data)
                        if form.cleaned_data['name'] ==  AdditionalName.objects.get(name="Otro"):
                            if not isNewName:
                                form.add_error("new_name", "El Campo Nombre es Requerido") 
                                continue
                            real_name = AdditionalName.objects.get_or_create(name=form.cleaned_data['new_name'].title())[0]
                            real_name.save()
                        else:
                            real_name = form.cleaned_data['name']
                        if 'description' in form.cleaned_data:
                            new_description = form.cleaned_data['description']
                        else:
                            new_description = ""

                        obj = AdditionalField(description=new_description, name=real_name)
                        obj.save()
                        program.additional_fields.add(obj.id)
                        program.save()
                    else:
                        print("What", form.cleaned_data)

                else:
                    print(form)

            # print(referenceForm.forms)
            # present_ref = []
            # for form in referenceForm.forms:
            #     if form.is_valid():
            #         if 'DELETE' in form.cleaned_data and form.cleaned_data['DELETE']:
            #             print("Quitando", form.cleaned_data['reference'])
            #             program.recommended_sources.remove(form.cleaned_data['reference'])
            #             program.save()
            #         else:
            #             print("Encontrado", form.cleaned_data['reference'])
            #             present_ref.append(form.cleaned_data['reference'])


            program_form_initial = {}
            # Lets select the right division if a department was chosen
            if program.department is not None:
                program_form_initial['division'] = Division.objects.filter(department__name=program.department)[0]
            program_form = ProgramForm(instance=program, initial=program_form_initial, prefix="program", error_class=DivErrorList)

    else:
        program_form_initial = {}
        
        # Lets select the right division if a department was chosen
        if program.department is not None:
            program_form_initial['division'] = Division.objects.filter(department__name=program.department)[0]
        
        program_form = ProgramForm(instance=program, initial=program_form_initial, prefix="program", error_class=DivErrorList)
        textstring_form = TextStringForm(instance=doc, prefix="textstring", error_class=DivErrorList)
        additionalFieldsForm = additionalFieldsFormset(initial=initial_fields, error_class=DivErrorList)
        #referenceForm = referenceFormset(initial=initial_refs, error_class=DivErrorList)


    render_dic['Name'] = doc.name
    render_dic['additionalFieldsForm'] = additionalFieldsForm
    render_dic['program_form'] = program_form
    #render_dic['ref_form'] = referenceForm
    render_dic['textstring_form'] = textstring_form

    return render(request, 'edit.html', render_dic)


def show_files(request):
    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'files.html',
        {'documents': documents}
    )


def sigpae(request):
    render_dic = {}
    results = []
    if request.method == "POST":
        search_form = SigpaeSearchForm(request.POST, error_class=DivErrorList)
        if search_form.is_valid():
            results = queries_sigpae(search_form.cleaned_data['code'].upper(), search_form.cleaned_data['trimester'], search_form.cleaned_data['year'])
            if len(results) == 0:
                search_form.add_error(None, "No se encontraron programas asociados en la búsqueda de " + search_form.cleaned_data['code'].upper())
    else:
        search_form = SigpaeSearchForm(error_class=DivErrorList)


    render_dic['search_form'] = search_form
    render_dic['results'] = results

    return render(
        request,
        'sigpae.html',
        render_dic
    )


def sigpae_show(request, pk):
    search = Programa.objects.filter(pk=pk)
    if len(search) != 0:
        render_dic = {'program' :  search[0]}
    else:
        render_dic = {'error' : 'Programa no encontrado'}
    
    return render(
        request,
        'sigpae_show.html',
        render_dic
    )

def sigpae_report(request):
    render_dic = {}
    resultT=None
    resultP=None
    if request.method == "POST":
        report_form = SigpaeReportForm(request.POST, error_class=DivErrorList)
        if report_form.is_valid():
            t = report_form.cleaned_data['report_type']
            c = str(report_form.cleaned_data['code'].code)
            if (t == 'Transcripciones'):
                resultT = report_transcriptions(c)
                if not resultT:
                    report_form.add_error(None, "No se encontraron transcripciones asociadas en la búsqueda de " + c)
            elif (t  == 'Programas'):
                resultP = report_programs(c)
                if not resultP:
                    report_form.add_error(None, "No se encontraron programas asociados en la búsqueda de " + c)
            else:
                resultT = report_transcriptions(c)
                resultP = report_programs(c)
                if not (resultT or resultP):
                    report_form.add_error(None, "No se encontraron transcripciones ni programas asociados en la búsqueda de " + c)
    else:
        report_form = SigpaeReportForm(error_class=DivErrorList)


    render_dic['report_form'] = report_form
    render_dic['resultT'] = resultT
    render_dic['resultP'] = resultP

    return render(
        request,
        'global_report.html',
        render_dic
    )


def ref_report(request):
    render_dic = {}
    results = []
    if request.method == "POST":
        report_form = RefReportForm(request.POST, error_class=DivErrorList)
        if report_form.is_valid():
            c = report_form.cleaned_data['code']
            t = report_form.cleaned_data['trimester']
            y = report_form.cleaned_data['year']
            if c:
                results = report_refs(c.code,t,y)
                if not results:
                    report_form.add_error(None, "No se encontraron fuentes de información vigentes para " + t + " " + y + " asociadas a " + c.code )
            else:
                results = report_refs(None,t,y)
                if not results:
                    report_form.add_error(None, "No se encontraron fuentes de información vigentes para " + t + " " + y )
    else:
        report_form = RefReportForm(error_class=DivErrorList)


    render_dic['report_form'] = report_form
    render_dic['results'] = results

    return render(
        request,
        'ref_report.html',
        render_dic
    )

def books(request):
    render_dic = {}
    render_dic['books'] = Reference.objects.all()
    return render(
        request,
        'books.html',
        render_dic
    )

def book_show(request, pk):
    render_dic = {}
    try:
        book = Reference.objects.get(pk=pk)
    except Exception as e:
        render_dic['error'] = "Referencia no encontrada"
        render_dic['title'] = "Referencia no encontrada"
        return render(
            request,
            'book.html',
            render_dic
        )

    authorFormSet = modelformset_factory(Author, exclude=(), can_delete=True, extra=0)

    if request.method == "POST":
        book_form = ReferenceForm(request.POST, instance=book, error_class=DivErrorList)
        author_form = authorFormSet(request.POST, queryset=book.author.all(), error_class=DivErrorList)
        if book_form.is_valid() and author_form.is_valid():
            book = book_form.save()
            authors = author_form.save() 
            for author in authors:
                if author not in book.author.all():
                    book.author.add(author)

            book.save()
    else:
        book_form = ReferenceForm(instance=book, error_class=DivErrorList)
        author_form = authorFormSet(queryset=book.author.all(), error_class=DivErrorList)

    render_dic['book'] = book_form
    render_dic['title'] = book.title
    render_dic['authorsForm'] = author_form
    render_dic['pk'] = book.pk
    return render(
        request,
        'book.html',
        render_dic
    )

def book_new(request):
    render_dic = {}
    authorFormSet = modelformset_factory(Author, exclude=(), can_delete=True, extra=0)
    if request.method == "POST":
        book_form = ReferenceForm(request.POST, error_class=DivErrorList)
        author_form = authorFormSet(request.POST, queryset=Author.objects.none(), error_class=DivErrorList)
        if book_form.is_valid() and author_form.is_valid():
            book = book_form.save(commit=True)
            authors = author_form.save(commit=True) 
            for author in authors:
                book.author.add(author)
            book.save()
            return HttpResponseRedirect(reverse(book_show, args=(str(book.pk),)))
        else:
            title = "Nueva Referencia"
    else:
        book_form = ReferenceForm(error_class=DivErrorList)
        author_form = authorFormSet(queryset=Author.objects.none(), error_class=DivErrorList)
        title = "Nueva Referencia"

    render_dic['book'] = book_form
    render_dic['title'] = title
    render_dic['authorsForm'] = author_form
    return render(
        request,
        'book.html',
        render_dic
    )
