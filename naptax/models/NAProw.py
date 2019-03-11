__author__ = 'nabeelh-dev'
from data.nap_csv_colMap import nap_csv_colMap

import json

class NAProw(object):
    def __init__(self, row_data):
        self._invoice_data = NAProw.generate_data(row_data)
        self._source_metainfo = {
                            "s_filename": None,
                            "source_rowNum": None
                            }

    def __repr__(self):
        return "<S/A/R:{}/{}/{} s_filename/row_num:{}/{}>".format(self._invoice_data.get("section"),
                                                                self._invoice_data.get("area"),
                                                                self._invoice_data.get("region"),
                                                                self.source_metainfo.get('s_filename'),
                                                                self.source_metainfo.get('source_rowNum'))

    @staticmethod
    def generate_data(raw_data):
        row_data = dict()
        for k, v in raw_data.items():
            # Dict.get() returns None if key not in
            # if mapped_key is None continue
            mapped_key = nap_csv_colMap.get(k)
            if not mapped_key : continue
            row_data[mapped_key] = v
        return row_data

    @property
    def source_metainfo(self):
        """

        :param source_meta: dict
        :return: None
        """
        return self._source_metainfo

    @source_metainfo.setter
    def source_metainfo(self, value_dict):
        for key in ["s_filename", 'source_rowNum']:
            if key not in value_dict.keys():
                raise ValueError("{} - Key not in source_metainfo dict!".format(key))
        for key, val in value_dict.items():
            self._source_metainfo[key] = val


    def toJSON(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)

    @property
    def invoice_data(self):
        return self._invoice_data

    @invoice_data.setter
    def invoice_data(self, value_dict):
        for key in value_dict.keys():
            if key not in self._invoice_data.keys():
                raise ValueError("{} - Key value not in invoice_data row!".format(key))
        for key in value_dict.keys():
            self._invoice_data[key] = value_dict[key]
