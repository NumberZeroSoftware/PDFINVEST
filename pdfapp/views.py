# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import Document, Program, Department, Division
from .forms import UploadFileForm, ProgramForm, TextStringForm

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

    # Lets see if they are sending the information or requesting it
    if request.method == "POST": 
        program_form = ProgramForm(request.POST, instance=program, prefix="program")
        textstring_form = TextStringForm(request.POST, instance=doc, prefix="textstring")
        
        if program_form.is_valid() and textstring_form.is_valid():
            program = program_form.save(commit=True)
            textstring_form.save(commit=True)
    else:
        program_form_initial = {}
        # Lets select the right division if a department was chosen
        if program.department is not None:
            program_form_initial['division'] = Division.objects.filter(department__name=program.department)[0]
        program_form = ProgramForm(instance=program, initial=program_form_initial, prefix="program")
        textstring_form = TextStringForm(instance=doc, prefix="textstring")

    render_dic['program_form'] = program_form
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
