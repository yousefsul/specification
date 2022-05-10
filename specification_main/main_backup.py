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
    print(col_names)
    global_var = GlobalVariables()
    header_section = global_var.get_header('new')
    final_result = {}
    header_sec = {}
    loop = segment = ""
    header_section.update({'835_id': 5642377248})
    final_result.update({'header_section': header_section})
    # final_result['Amount Qualifier Code'] = {}
    # final_result['2110'] = {}
    # final_result['2110']['AMT'] = {}
    # final_result['2110']['AMT']["442"] = {}

    for count, row in df.iterrows():
        specification_info = SpecificationInfo(df.loc[count])

        # result = {
        #     specification_info.get_code(): specification_info.get_definition(),
        # }
        # final_result['Amount Qualifier Code'].update(result)

        if specification_info.get_data_element_id() == "":
            loop = specification_info.get_loop()
            segment = specification_info.get_segment_id()
            if loop not in final_result.keys():
                header_sec[specification_info.get_loop()] = {}
        elif re.search('-', specification_info.get_data_element_id()) and \
                specification_info.get_data_element_id().split('-')[0] == list(final_result.keys())[-1]:
            sub_result = {
                specification_info.get_data_element_id(): {
                    'listed_order': specification_info.get_listed_order(),
                    'loop': specification_info.get_loop(),
                    'segment_id': specification_info.get_segment_id(),
                    'data_element': specification_info.get_data_elements(),
                    'data_element_name': specification_info.get_data_element_name(),
                    'implementation_name': specification_info.get_implementation_name(),
                    'medvertex_label': specification_info.get_medvertex_label(),
                    'need_description': specification_info.get_need_description(),
                    'min_length': specification_info.get_min_length(),
                    'max_length': specification_info.get_max_length(),
                    'value': specification_info.get_value(),
                    'data_type': specification_info.get_data_type(),
                    'format': specification_info.get_format(),
                    'required': specification_info.get_required(),
                    'notes': specification_info.get_notes_comments()
                }
            }
            header_sec[loop][segment].get(list(list(final_result.keys())[-1])).update(sub_result)
            final_result.get(list(final_result.keys())[-1]).update(sub_result)
        else:
            header_sec[specification_info.get_loop()][specification_info.get_segment_id()] = {}
            result = {
                # specification_info.get_data_element_id(): {
                #     'listed_order': specification_info.get_listed_order(),
                #     'loop': specification_info.get_loop(),
                #     'segment_id': specification_info.get_segment_id(),
                'names': {
                    'data_element_name': specification_info.get_data_element_name(),
                    'implementation_name': specification_info.get_implementation_name(),
                    'medvertex_label': specification_info.get_medvertex_label(),
                },
                'data_element': specification_info.get_data_elements(),
                # 'need_description': specification_info.get_need_description(),
                'length': {
                    'min': specification_info.get_min_len(),
                    'max': specification_info.get_max_len(),
                },
                # 'min_length': specification_info.get_min_length(),
                # 'max_length': specification_info.get_max_length(),
                'repeat': specification_info.get_repeat(),
                'values': specification_info.get_values(),
                # 'value': specification_info.get_value(),
                'data_type': specification_info.get_data_type(),
                'format': specification_info.get_format(),
                'required': specification_info.get_required(),
                'notes': specification_info.get_notes_comments()
                # }
            }
            header_sec[loop][segment][specification_info.get_data_element_id()] = result
            final_result.update(header_sec)

        # if specification_info.get_data_element_id() == "":
        #         break
        # elif re.search('-', specification_info.get_data_element_id()) and \
        #         specification_info.get_data_element_id().split('-')[0] == list(final_result.keys())[-1]:
        #     sub_result = {
        #         specification_info.get_data_element_id(): {
        #             'listed_order': specification_info.get_listed_order(),
        #             'loop': specification_info.get_loop(),
        #             'segment_id': specification_info.get_segment_id(),
        #             'data_element': specification_info.get_data_elements(),
        #             'data_element_name': specification_info.get_data_element_name(),
        #             'implementation_name': specification_info.get_implementation_name(),
        #             'medvertex_label': specification_info.get_medvertex_label(),
        #             'need_description': specification_info.get_need_description(),
        #             'min_length': specification_info.get_min_length(),
        #             'max_length': specification_info.get_max_length(),
        #             'value': specification_info.get_value(),
        #             'data_type': specification_info.get_data_type(),
        #             'format': specification_info.get_format(),
        #             'required': specification_info.get_required(),
        #             'notes': specification_info.get_notes_comments()
        #         }
        #     }
        #     final_result.get(list(final_result.keys())[-1]).update(sub_result)
        #     result = {
        #         specification_info.get_data_element_id(): {
        #             'listed_order': specification_info.get_listed_order(),
        #             'loop': specification_info.get_loop(),
        #             'segment_id': specification_info.get_segment_id(),
        #             'data_element': specification_info.get_data_elements(),
        #             'data_element_name': specification_info.get_data_element_name(),
        #             'implementation_name': specification_info.get_implementation_name(),
        #             'medvertex_label': specification_info.get_medvertex_label(),
        #             'need_description': specification_info.get_need_description(),
        #             'min_length': specification_info.get_min_length(),
        #             'max_length': specification_info.get_max_length(),
        #             'value': specification_info.get_value(),
        #             'data_type': specification_info.get_data_type(),
        #             'format': specification_info.get_format(),
        #             'required': specification_info.get_required(),
        #             'notes': specification_info.get_notes_comments()
        #         }
        #     }
        #     final_result.update(result)
    print(json.dumps(final_result, indent=4))
    # # connection.update_one_document_using_key("_id", ObjectId("61d40a48dd22a6493427e5d5"), final_result)
    connection.insert_to_collection(final_result)


if __name__ == '__main__':
    # extract_information_reference_table()
    extract_information_specification_table()
    # connection = ConnectMongoDB('devDB')
    # connection.connect_to_collection('Specification835')
    # x = connection.find_from_collection()
    # for i in x:
    #     i.pop('_id')
    #     print(json.dumps(i , indent=4))

# ['ID', 'Listed Order', 'LOOP', 'SEGMENT', 'DATA ELEMENT', 'NAME', 'Implementation Name', 'MEDVERTEX LABEL', 'ELEMENT LENGTH', 'Length\nMax', 'REPEAT', 'VALUES', 'DATA TYPE', 'Format', 'USAGE', 'RULES']