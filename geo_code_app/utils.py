import xlrd
import xlwt
import googlemaps
from datetime import datetime
from django.conf import settings

from geo_code_app.models import GeoFileUpload


def process_file(geo_file_obj):
    '''Proces the excel address file.
    
    Method to fetch address data from excel 
    sheet then find geocode for that 
    address and store lat and lng of that address in excel file. 
    xlrd is used to fetch data from excel.
    xlwt is used to create new excel workbook.
    googlemaps is used for finding lat and lng.
    
    :param geo_file_obj: Model File object. 
    '''
    file_path = geo_file_obj.file_path
    file_name = geo_file_obj.new_file_name
    upload_file_name = file_path + file_name

    wb = xlrd.open_workbook(upload_file_name)
    excel_file = xlwt.Workbook()
    sheet_w = excel_file.add_sheet('address')

    row = 1
    sheet_w.write(0, 0, "Address")
    sheet_w.write(0, 1, "City")
    sheet_w.write(0, 2, "State")
    sheet_w.write(0, 3, "Country")
    sheet_w.write(0, 4, "Pin Code")
    sheet_w.write(0, 5, "Latitude")
    sheet_w.write(0, 6, "Longitude")
    sheet = wb.sheet_by_index(0)
    gmaps = googlemaps.Client(key=settings.GEO_API_KEY)
    # Geocoding an address

    for i in range(sheet.nrows):
        '''Fetch address one by one and find lat and lng
        for that address and put that in respective rows
        '''
        if i == 0:
            continue
        address = sheet.cell_value(i, 0)
        city = sheet.cell_value(i, 1)
        state = sheet.cell_value(i, 2)
        country = sheet.cell_value(i, 3)
        pin = sheet.cell_value(i, 4)
        full_address = "{0} {1} {2} {3} {4} ".format(
            address, city, state, country, pin)

        # Find lat lng for given address
        geocode_result = gmaps.geocode(full_address)
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        # write data in new workbook
        sheet_w.write(row, 0, address)
        sheet_w.write(row, 1, city)
        sheet_w.write(row, 2, state)
        sheet_w.write(row, 3, country)
        sheet_w.write(row, 4, pin)
        sheet_w.write(row, 5, lat)
        sheet_w.write(row, 6, lng)

        row += 1
    # save workbook to upload file 
    excel_file.save(upload_file_name)


def handle_uploaded_file(f, filename, file_path):
    '''Upload the excel address file.

        Parameter:
        f - file object.
        filename - name of file.
        file_path - path of file where the file is stored in server.

        Create new excel file in server with name
        having address and date time. After that read data
        in chunck from upload file and put it in new excel file.

        return upload status and geo_file object
    '''
    try:
        file_splited_arr = filename.split('.')
        file_extension = file_splited_arr[-1]
        # setting the file name to be stored.
        file_name = 'address-{0}'.format(datetime.now())
        file_name = file_name.replace('.', '')
        file_name = file_name.replace(':', '')
        file_name = '{0}.{1}'.format(file_name, file_extension)
        upload_file_name = file_path + file_name
        # write file content chunck by chunck 
        with open(upload_file_name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        # save file details in database table
        geo_file_obj = GeoFileUpload()
        geo_file_obj.file_name = filename
        geo_file_obj.new_file_name = file_name
        geo_file_obj.file_path = file_path
        geo_file_obj.save()

        return True, geo_file_obj

    except Exception as e:
        print e
        return False, False


def get_file_list():
    '''Fetch all file list from database table in list
        return list of dictionary having id and file name
    '''
    geo_file_list = []
    geo_file_objs = GeoFileUpload.objects.values_list(
        'pk_id', 'file_name').filter(is_active=True)

    for geo_file_obj in geo_file_objs:
        geo_file_dic = {
            'id': geo_file_obj[0],
            'file_name': geo_file_obj[1]
        }

        geo_file_list.append(geo_file_dic)

    return geo_file_list
