__author__ = 'nabeelh-dev'
from data.col_mapping import csv_columnSettings

import json

class NAProw(object):
    def __init__(self, row_data):
        self.invoice_data = NAProw.generate_data(row_data)
        self.source_meta = {
                            "s_filename": None,
                            "row_num": None
                            }

    def __repr__(self):
        return "<S/A/R:{}/{}/{} s_filename/row_num:{}/{}>".format(self.section,
                                                                 self.area,
                                                                 self.source_meta.get('s_filename'),
                                                                 self.source_meta.get('row_num'))
    @staticmethod
    def generate_data(raw_data):
        row_data = dict()
        for k, v in raw_data.items():
            # Dict.get() returns None if key not in
            # So columns will only be loaded if defined in col_mapping.py
            mapped_key = csv_columnSettings.get(k)
            if not mapped_key: continue
            row_data[mapped_key] = v
        return row_data


    def _update_source_metainfo(self, source_meta):
        """

        :param source_meta: dict
        :return: None
        """
        self.source_meta = dict(source_meta)

    def toJSON(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)

