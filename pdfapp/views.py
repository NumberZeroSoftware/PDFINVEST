# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Document
from .forms import UploadFileForm

from datetime import date


def upload_view(request):
    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #print('valid')
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
    # Load documents to search for the requested file
    documents = Document.objects.all()
    try:
        doc = next(filter(lambda document: document.docfile.name == full_filePath, documents))
    except StopIteration:
        render_dic['error'] = 'File not found.'
    render_dic['doc'] = doc
    render_dic['fileName'] = fileName
    #path = call_main(filePath + "/" + full_filePath)
    path = 'media/test.html'
    render_dic['html_string'] = open(path, 'r').read()
    return render(request, 'edit.html', render_dic)
