# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import Document, Program, Department
from .forms import UploadFileForm, ProgramForm

from datetime import date
from pathlib import Path
import re
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
    #Calculate the number of years between 1969 and the present
    render_dic['years'] = [i for i in range(date.today().year, 1968, -1)]
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
    except StopIteration:
        render_dic['error'] = 'Error: File not found.'
        render_dic['html_string'] = 'Error: File not found.'
        return render(request, 'edit.html', render_dic)
    
    # Lets see if the html file is ready
    if html_file is not None:
        # Lets see if it really exists
        if Path(html_file).is_file():
            with open(html_file, 'r') as f:
                render_dic['html_string'] = f.read()
            doc.processing_html = False
            doc.ready_html = True
            doc.save()
        else:
            render_dic['html_string'] = 'File is being created. Please be patient.'
            render_dic['reload'] = True
            doc.ready_html = False
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
    print("---------------")

    program = Program.objects.get_or_create(document=doc)[0]

    # if request.method == "POST":
    #     program.department = Department.objects.get(pk=request.POST['department'])
    #     program.code = request.POST['code']
    #     program.validity_trimester = request.POST['validity_trimester']
    #     program.validity_year = int(request.POST['validity_year'])
    #     program.objectives = request.POST['objectives']
    #     program.save()

    # render_dic['program'] = program
    # render_dic['departments'] = Department.objects.all()
    # render_dic['trimesters'] = ['Ene-Mar', 'Abr-Jul', 'Jul-Ago', 'Sep-Dic']
    # return render(request, 'edit.html', render_dic)

    if request.method == "POST":
        program_form = ProgramForm(request.POST, instance=program)
        
        if program_form.is_valid():
            program = program_form.save(commit=True)
        #else:
    else:
        program_form = ProgramForm(instance=program)

    render_dic['program_form'] = program_form
    render_dic['departments'] = Department.objects.all()
    render_dic['trimesters'] = ['Ene-Mar', 'Abr-Jul', 'Jul-Ago', 'Sep-Dic']
    return render(request, 'edit.html', render_dic)
