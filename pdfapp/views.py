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
    years = []
    i = date.today().year
    while 1969 <= i:
        years.append(i)
        i -= 1
    render_dic['years'] = years
    # Load documents to search for the requested file
    documents = Document.objects.all()
    for doc in documents:
        # If we got this doc we send it
        if doc.docfile.name == full_filePath:
            render_dic['doc'] = doc
            render_dic['fileName'] = fileName
            break
    return render(request, 'edit.html', render_dic)