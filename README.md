# Props_Assignment
Develop a simple 1 page Django application that does the following:
Allows user to upload an Excel sheet with address fields. One or more rows allowed.
The system should use these address fields and using Google Geocoding API, get the latitude and longitude of that address.
The system then provides an excel download of the address excel with latitude and longitude fields appended to each row.


To setup the project pull code from git repository and add new file local_settings.py under Props_Assignment->Props_Assignment

In local settings.py add 

GEO_API_KEY = "api_key_here"

Replace "api_key_here" with google geo code api key.

In this project I have used following package:
xlrd:- for reading excel data
xlwt:- writing data to excel file
googlemaps:- for finding lat and lng
