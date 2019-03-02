from naptax.models.NAProw import NAProw
from naptax.models.utils import sortDates, getUniqueCounts
import csv
import os


class NAPcollection(object):
    def __init__(self, csv_path, csv=True):
        self.filepath = csv_path
        self.rows = self.parse_csv() if csv else self.parse_json()


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

        # directory input, process all .csv contained within directory
        dirpath = os.path.dirname(__file__)
        csv_dp = os.path.join(dirpath, "../../" + self.filepath)
        for filename in os.listdir(csv_dp):
            if filename.endswith(".csv"):
                filepath = os.path.join(csv_dp, filename)
                for _NAProw in NAPcollection._parse_single_csv(filepath):
                    NAProw_list.append(_NAProw)

        return NAProw_list

    @staticmethod
    def _parse_single_csv(csv_fp):
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
            for i in range(0, 5, 1):
                next(csv_file, None)
            # Enumerate dict to calculate length of lines
            data = dict(enumerate(csv.DictReader(csv_file)))
            print("{} lines in csv file.".format(len(data)))

            _NAProw_list = list()
            for i in range(0, len(data)):
                temp_row = NAProw(data[i])
                temp_row.generate_data()
                _NAProw_list.append(temp_row)

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
        date_list = [row.trxdate for row in self.rows]
        return sortDates(date_list)

    # Gets earliest and latest invoice trx date in collection
    def getPostingDateRange(self):
        date_list = [row.gldate for row in self.rows]
        return sortDates(date_list)

    # Gets dict counts of all GL account codes
    def getGLCodes(self):
        gl_list = [row.glacct for row in self.rows]
        return getUniqueCounts(gl_list)

    # Gets dict counts of all region codes
    def getRegionCodes(self):
        region_codes = [row.region for row in self.rows]
        return getUniqueCounts(region_codes)

    # Gets dict counts of all area codes
    def getAreaCodes(self):
        area_codes = [row.area for row in self.rows]
        return getUniqueCounts(area_codes)

    # Gets dict counts of all section codes
    def getSectionCodes(self):
        section_codes = [row.section for row in self.rows]
        return getUniqueCounts(section_codes)

    # Outputs invoices grouped by chosen SAR level and in Excel/GP format.
    def groupInvoicesBy(self, bySAR=None, gpOutput="r", excelOutput=True):
        pass