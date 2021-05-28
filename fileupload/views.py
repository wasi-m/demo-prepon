from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.contrib import messages
import re
import pandas as pd
from django.conf import settings
from sqlalchemy import create_engine

database_name = settings.DATABASES['default']['NAME']
engine = create_engine(f'sqlite:///{database_name}')



def index(request):
    if "GET" == request.method:
        return render(request, 'index.html')
    else:
        # this is the regex expression to search on
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size
        dataframe = pd.read_excel(excel_file, index_col=None)

        dataframe['isemail'] = dataframe['Email'].apply(lambda x: True if pattern.match(x) else False)

        # if dataframe['Sr. No'].dtype != int:
        #     messages.add_message(request, messages.INFO, 'Sr. No info is incorrect.')
        messages.add_message(request, messages.INFO, '')
        if dataframe.empty:
            messages.add_message(request, messages.INFO, 'Empty value not allowed.')
        elif isinstance(dataframe['Batch'].dtype, str):
            messages.add_message(request, messages.INFO, 'Batch info is incorrect.')
        elif isinstance(dataframe['First Name'].dtype, str):
            messages.add_message(request, messages.INFO, 'First Name info is incorrect.')
        elif isinstance(dataframe['Last Name'].dtype, str):
            messages.add_message(request, messages.INFO, 'Last Name info is incorrect.')
        elif not dataframe['isemail'].all():
            messages.add_message(request, messages.INFO, 'Email info is incorrect.')
        elif dataframe['Contact'].dtype !=  int:
            messages.add_message(request, messages.INFO, 'Contact info is incorrect.')
        else:
            messages.add_message(request, messages.INFO, 'File is correct. Uploading file to database!')

        # remove sr no and isemail
        dataframe = dataframe.drop(['Sr. No', 'isemail'], axis=1)

        # arange column names
        dataframe = dataframe.rename(columns=str.lower)
        dataframe = dataframe.rename(columns = {'first name':'first_name'})
        dataframe = dataframe.rename(columns = {'last name':'last_name'})
        print(dataframe)
        dataframe.to_sql('fileupload_student', engine, if_exists='append', index=False)

        messages.add_message(request, messages.INFO, 'File uploaded in database')

        return render(request, 'index.html')