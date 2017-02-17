# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import Document
from .forms import UploadFileForm

from datetime import date

from utils.shell import call_main


def upload_view(request):
    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
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
# fileName is the name of the file
# filePath is the file path of the pdf to edit
# TODO: better send file names rather than this
def edit_view(request, fileName, filePath=None,):
    render_dic = {}
    full_filePath = fileName
    if filePath is not None:
        full_filePath = filePath + "/" + full_filePath
    #Calculate the number of years between 1969 and the present
    render_dic['years'] = [i for i in range(date.today().year, 1968, -1)]
    #Save fileName
    render_dic['fileName'] = fileName
    # Load documents to search for the requested file
    documents = Document.objects.all()
    html_file = None
    render_dic['html_string_status'] = 0
    render_dic['html_string'] = 'File is being created. Please be patient.'
    try:
        doc = next(filter(lambda document: document.docfile.name == full_filePath+".pdf", documents))
        render_dic['doc'] = doc
        #Process file
        if not doc.ready_html:
            html_file = call_main(doc.docfile.path)
            doc.processing_html = True
    except StopIteration:
        render_dic['error'] = 'Error: File not found.'
        render_dic['html_string'] = 'Error: File not found.'
        return render(request, 'edit.html', render_dic)
    
    # Lets see if the html file is ready
    if html_file is not None:
        try:
            render_dic['html_string'] = open(html_file, 'r').read()
            render_dic['html_string_status'] = 1
            doc.processing_html = False
            doc.ready_html = True
        except Exception as e:
            render_dic['html_string'] = 'File is being created. Please be patient.'
        
    return render(request, 'edit.html', render_dic)
