from naptax.models.NAProw import NAProw
from naptax.models.utils import getMinMaxDates, getUniqueCounts

import csv
import os
from functools import reduce


class NAPcollection(object):
    def __init__(self, csv_path, csv=True):
        self.filepath = csv_path
        self.naprows = self.parse_csv() if csv else self.parse_json()


    def parse_csv(self):
        """
        If self.filename is a directory object then load data from all csv's inside.
        If csv then load data from csv.
        :input: self
        :return: NAProw_list : list of NAProw objects
        """
        NAProw_list = list()

        # If self.rows has data already, return error so
        # can be sure loading processes only happens when first loaded?

        # if input is just a csv file, process and return
        if self.filepath.endswith(".csv"):
            # construct filepath using self.csv_fp
            dirpath = os.path.dirname(__file__)
            csv_fp = os.path.join(dirpath, "../../" + self.filepath)
            return NAPcollection._parse_single_csv(csv_fp)

        # for dir at dirpath process all .csv contained within
        dirpath = os.path.dirname(__file__)
        csv_dp = os.path.join(dirpath, "../../" + self.filepath)
        for filename in os.listdir(csv_dp):
            if filename.endswith(".csv"):
                csv_fp = os.path.join(csv_dp, filename)
                for NAProw in NAPcollection._parse_single_csv(csv_fp, filename):
                    NAProw_list.append(NAProw)

        return NAProw_list

    @staticmethod
    def _parse_single_csv(csv_fp, filename=None):
        """
        Takes filepath, opens CSV, skips first 5 lines,
        Reads each row and loads as a NAProw object.
        Appends to a list which is returned.
        :param csv_fp: str
        :return: _NAProw_list : list of NAProw objects
        """
        with open(csv_fp) as csv_file:
            print("Opened CSV Successfully: {}".format(str(csv_fp)))
            # Skip the first 6 lines of csv file due to header
            ## IMPLEMENT passing down file header data, look into CSV class functions
            for i in range(0, 5, 1):
                next(csv_file, None)
            # Enumerate dict to calculate length of lines in csv.
            data = dict(enumerate(csv.DictReader(csv_file)))
            print("{} lines in csv.".format(len(data)))

            _NAProw_list = list()
            for i in range(0, len(data)):
                _NAProw = NAProw(data[i])
                _NAProw._update_source_metainfo({
                                                's_filename': filename,
                                                'source_rowNum': str(i)
                                                })
                _NAProw_list.append(_NAProw)

        return _NAProw_list

    def parse_json(self):
        """
        For loading archived data.
        :return:
        """
        pass

    @staticmethod
    def _parse_single_json(json_fp):
        """
        Loads a single .json backup file.
        :param json_fp:
        :return:
        """
        pass

    def processSalesTax(self):
        pass

    # Gets earliest and latest invoice trx date in collection
    def getTRXDateRange(self):
         date_list = [row.invoice_data['trxDate'] for row in self.naprows]
         return getMinMaxDates(date_list)



    # Gets earliest and latest invoice trx date in collection
    def getPostingDateRange(self):
        date_list = [row.invoice_data['glDate'] for row in self.naprows]
        return getMinMaxDates(date_list)

    # Gets dict counts of all GL account codes
    def getGLCodes(self):
        gl_list = [row.invoice_data['glAcct'] for row in self.naprows]
        return getUniqueCounts(gl_list)

    # Gets dict counts of all region codes
    def getRegionCodes(self):
        region_codes = [row.invoice_data['region'] for row in self.naprows]
        return getUniqueCounts(region_codes)

    # Gets dict counts of all area codes
    def getAreaCodes(self):
        area_codes = [row.invoice_data['area'] for row in self.naprows]
        return getUniqueCounts(area_codes)

    # Gets dict counts of all section codes
    def getSectionCodes(self):
        section_codes = [row.invoice_data['section'] for row in self.naprows]
        return getUniqueCounts(section_codes)

    # Gets unique file sources in collection
    def getFileSources(self):
        file_sources = [row.source_meta.get('s_filename') for row in self.naprows]
        return getUniqueCounts(file_sources)

    # Outputs invoices grouped by chosen SAR level and in Excel/GP format.
    def groupInvoicesBy(self, bySAR=None, gpOutput="r", excelOutput=True):
        pass