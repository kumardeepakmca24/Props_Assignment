# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str

from geo_code_app.forms import GeoFileUploadForm
from geo_code_app.models import GeoFileUpload
from geo_code_app.utils import get_file_list, process_file, \
    handle_uploaded_file


def upload_geo_file(request):
    '''Used to upload geo address file and load html page

       If request method is post it will upload the file. and then call
       process_file method based upon the upload status returned from
       handle_uploaded_file method.
       If request is not POST then load html template.
       Html template will render all geo file uploaded and also the
       upload form.
    '''
    error = ''
    if request.method == 'POST':
        # validate the upload form
        form = GeoFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = request.FILES['file']
            file_name = file_obj.name
            file_path = 'static/uploads/'
            # Method used to handle file upload
            # returned status is checked for file upload status
            status, geo_file_obj = handle_uploaded_file(
                file_obj, file_name, file_path
            )
            if status:
                # method used to fetch data from file and
                # find geo location and append that into the file
                process_file(geo_file_obj)
            else:
                error = "Something went wrong: Please check uploaded file."
    else:
        form = GeoFileUploadForm()

    # Get file list from db
    geo_file_list = get_file_list()
    context = {
        'form': form,
        'geo_file_list': geo_file_list,
        'error': error
    }

    return render(request, 'geo_upload.html', context)


def download_address_file(request, id):
    '''Download address file

        Parameter:
        id - file id store in dtatabase

        fetch the file and send excel file in response to download
    '''
    geo_file_obj = GeoFileUpload.objects.get(pk_id=id)
    doc_abs_path = os.path.join(
        settings.MEDIA_ROOT,
        geo_file_obj.file_path,
        geo_file_obj.new_file_name
    )
    response = HttpResponse(
        open(doc_abs_path, "rb"),
        content_type='application/force-download'
    )
    url = os.path.join(geo_file_obj.file_path, geo_file_obj.new_file_name)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        smart_str(str(geo_file_obj.file_name))
    )
    length = os.path.getsize(doc_abs_path)
    response['Content-Length'] = str(length)
    response['X-Accel-Redirect'] = url

    return response


def downlopad_sample_file(request):
    '''Download sample file

       Send the sample file as response
    '''
    doc_abs_path = os.path.join(
        settings.MEDIA_ROOT,
        "static/uploads/",
        "sample.xls"
    )
    response = HttpResponse(
        open(doc_abs_path, "rb"),
        content_type='application/force-download'
    )
    url = os.path.join("static/uploads/", "sample.xls")
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        smart_str(str("sample.xls"))
    )
    length = os.path.getsize(doc_abs_path)
    response['Content-Length'] = str(length)
    response['X-Accel-Redirect'] = url

    return response
