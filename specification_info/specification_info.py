import math


class SpecificationInfo:
    def __init__(self, specification_info):
        self.__specification_info = specification_info

    def get_data_element_id(self):
        return str(self.__specification_info.get("ID"))

    def get_listed_order(self):
        if self.__specification_info.get("Listed Order") == "":
            return ""
        if self.__specification_info.get("Listed Order") % 1 == 0:
            return int(self.__specification_info.get("Listed Order"))
        else:
            return self.__specification_info.get("Listed Order")

    def get_loop(self):
        return str(self.__specification_info.get("LOOP")).strip()
        # return str(self.__specification_info.get("Loop ID")).strip()

    def get_segment_id(self):
        return str(self.__specification_info.get("SEGMENT")).strip()
        # return str(self.__specification_info.get("Segment ID")).strip()

    def get_data_elements(self):
        return str(self.__specification_info.get("DATA ELEMENT")).strip()

    def get_data_element_name(self):
        return str(self.__specification_info.get("NAME")).strip()
        # return str(self.__specification_info.get("Data Element Name")).strip()

    def get_implementation_name(self):
        return str(self.__specification_info.get("Implementation Name")).strip()

    def get_min_length(self):
        if self.__specification_info.get("Length\nMin"):
            return int(self.__specification_info.get("Length\nMin"))
        else:
            return 0

    def get_max_length(self):
        if self.__specification_info.get("Length\nMax"):
            return int(self.__specification_info.get("Length\nMax"))
        else:
            return 0

    def get_value(self):
        return str(self.__specification_info.get("Value")).strip()

    def get_data_type(self):
        return str(self.__specification_info.get("Data Type")).strip()
        # return str(self.__specification_info.get("Data Type\n")).strip()

    def get_format(self):
        return str(self.__specification_info.get("Format"))

    def get_required(self):
        return str(self.__specification_info.get("USAGE")).strip()
        # return str(self.__specification_info.get("Data Element Usage\nRequired or Situational")).strip()

    def get_notes_comments(self):
        return str(self.__specification_info.get("RULES")).strip()
        # return str(self.__specification_info.get("Notes/Comments")).strip()

    def get_code(self):
        return str(self.__specification_info.get("Code")).strip()

    def get_definition(self):
        return str(self.__specification_info.get("Definition")).strip()

    def get_explanation(self):
        return str(self.__specification_info.get("Explanation")).strip()

    def get_medvertex_label(self):
        return str(self.__specification_info.get("Medvertex Label")).strip()

    def get_need_description(self):
        return str(self.__specification_info.get("Need Description")).strip()

    def get_min_len(self):
        if self.__specification_info.get("ELEMENT LENGTH"):
            return int(self.__specification_info.get("ELEMENT LENGTH").split('/')[0])
        else:
            return 0

    def get_max_len(self):
        if self.__specification_info.get("ELEMENT LENGTH"):
            return int(self.__specification_info.get("ELEMENT LENGTH").split('/')[1])
        else:
            return 0

    def get_repeat(self):
        return self.__specification_info.get("REPEAT")

    def get_values(self):
        if self.__specification_info.get("VALUES"):
            return self.__specification_info.get("VALUES")
        else:
            ""

