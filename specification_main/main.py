import glob
import json
import re

import numpy as np
import pandas as pd
import tabula
from application.ConnectMongoDB import ConnectMongoDB
from bson import ObjectId
from tabula import read_pdf

from specification_info.specification_info import SpecificationInfo
from application.GlobalVariables import GlobalVariables
from application.CommnMethodUsed import CommonMethodUsed
import camelot


def get_request_files():
    return glob.glob(pathname='../files/*')


def extract_information_reference_table():
    path = 'C:/Users/yousef/Desktop/Medvertex/separated/specification/files/request/Florida-Health-Care-Plans-835.pdf'
    # tabula.convert_into(path, "reference_table.csv", output_format="csv", pages="all")
    # tabula.convert_into(path, "reference_table.json", output_format="json", pages="all")

    # file1 = "https://www.fhcp.com/documents/forms/Florida-Health-Care-Plans-835.pdf.pdf"
    # table = tabula.read_pdf(file1, pages="all")
    # print(table)

    from tabula import read_pdf
    from tabulate import tabulate

    # reads table from pdf file
    df = read_pdf(path, pages="all")  # address of pdf file

    print(dir(df))
    for i in df:
        print(i)
        break

    # for i in df:
    #     print(i.to_dict())
    # print(type(df))
    #
    # print()
    # print(dir(df))
    # print(dir(tabulate(df)))
    # print(tabulate(df))


def insert_as_sub_data_element():
    pass


def extract_information_specification_table():
    spec_file = 'C:/Users/yousef/Desktop/Medvertex/separated/specification/files/request/835 Health Care Claim Payment_Updated.xlsx'
    connection = ConnectMongoDB('devDB')
    connection.connect_to_collection('Specification835')
    df = pd.read_excel(spec_file, sheet_name='Data Elements', na_filter=False).replace(np.nan, '', regex=True)

    # df = pd.read_excel(spec_file, sheet_name='Ref.Table_442_AMT01').replace(np.nan, '', regex=True)
    col_names = df.columns.to_list()
    # print(col_names)
    global_var = GlobalVariables()
    header_section = global_var.get_header('new')
    final_result = {}
    header_sec = {}
    segment_count = 0
    loop = segment = ""
    header_section.update({'835_id': 5642377248})
    # final_result.update({'header_section': header_section})
    # final_result['Amount Qualifier Code'] = {}
    x = c = 1
    for count, row in df.iterrows():
        specification_info = SpecificationInfo(df.loc[count])

        if specification_info.get_data_element_id() == "" and x == 1:
            loop = specification_info.get_loop()
            segment = specification_info.get_segment_id()
            if specification_info.get_loop() not in final_result.keys():
                if x == 1:
                    header_sec[specification_info.get_loop()] = {}
                    info = {
                        'name': specification_info.get_data_element_name(),
                        'repeat': specification_info.get_repeat(),
                        'usage': specification_info.get_required()
                    }
                    header_sec[specification_info.get_loop()]['info'] = info
                    x += 1
                    c = 1

        elif re.search('-', specification_info.get_data_element_id()) and \
                specification_info.get_data_element_id().split('-')[0] == list(final_result[loop][segment].keys())[-1]:
            sub_result = {
                specification_info.get_data_element_id(): {
                    #     'listed_order': specification_info.get_listed_order(),
                    #     'loop': specification_info.get_loop(),
                    #     'segment_id': specification_info.get_segment_id(),
                    'names': {
                        'data_element_name': specification_info.get_data_element_name(),
                        'implementation_name': specification_info.get_implementation_name(),
                        'medvertex_label': specification_info.get_medvertex_label(),
                    },
                    'data_element': specification_info.get_data_elements(),
                    'length': {
                        'min': specification_info.get_min_len(),
                        'max': specification_info.get_max_len(),
                    },
                    'repeat': specification_info.get_repeat(),
                    'values': specification_info.get_values(),
                    'data_type': specification_info.get_data_type(),
                    'format': specification_info.get_format(),
                    'required': specification_info.get_required(),
                    'notes': specification_info.get_notes_comments()
                }
            }
            header_sec[loop][segment]['394'].update(sub_result)
            # print(header_sec[loop][segment])
            # header_sec[loop][segment].get(list(final_result.keys())[-1]).update(sub_result)
            # final_result.get(list(final_result.keys())[-1]).update(sub_result)
        else:
            x = 1
            if specification_info.get_segment_id() not in header_sec[loop]:
                segment = specification_info.get_segment_id()
                header_sec[loop][segment] = {}
                if c == 1:
                    info = {
                        'name': specification_info.get_data_element_name(),
                        'repeat': specification_info.get_repeat(),
                        'usage': specification_info.get_required()
                    }
                    header_sec[loop][segment]['info'] = info
                    c += 1
                    continue
            result = {
                specification_info.get_data_element_id(): {
                    #     'listed_order': specification_info.get_listed_order(),
                    #     'loop': specification_info.get_loop(),
                    #     'segment_id': specification_info.get_segment_id(),
                    'names': {
                        'data_element_name': specification_info.get_data_element_name(),
                        'implementation_name': specification_info.get_implementation_name(),
                        'medvertex_label': specification_info.get_medvertex_label(),
                    },
                    'data_element': specification_info.get_data_elements(),
                    'length': {
                        'min': specification_info.get_min_len(),
                        'max': specification_info.get_max_len(),
                    },
                    'repeat': specification_info.get_repeat(),
                    'values': specification_info.get_values(),
                    'data_type': specification_info.get_data_type(),
                    'format': specification_info.get_format(),
                    'required': specification_info.get_required(),
                    'notes': specification_info.get_notes_comments()
                }
            }
            header_sec[loop][segment].update(result)
            final_result.update(header_sec)
    print(json.dumps(final_result, indent=4))
    connection.insert_to_collection(final_result)


if __name__ == '__main__':
    # extract_information_reference_table()
    extract_information_specification_table()

# ['ID', 'Listed Order', 'LOOP', 'SEGMENT', 'DATA ELEMENT', 'NAME', 'Implementation Name', 'MEDVERTEX LABEL', 'ELEMENT LENGTH', 'Length\nMax', 'REPEAT', 'VALUES', 'DATA TYPE', 'Format', 'USAGE', 'RULES']
