from naptax.models.NAPRow import NAPRow
from naptax.models.utils import sortDates, getUniqueCounts
import csv
import os


class NAPCollection(object):
    def __init__(self, csv_filepath):
        self.filename = csv_filepath
        self.rows = self.parse_file()


    def parse_file(self):
        dirpath = os.path.dirname(__file__)
        filepath = os.path.join(dirpath, '../../'+self.filename)

        with open(filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            print("Opened CSV Successfully: {}".format(self.filename.split('/')[2]))

            # Skip the first 6 lines of csv file due to header
            for i in range(0,5,1):
                next(csv_file, None)

            data = dict(enumerate(csv.DictReader(csv_file)))
            print("{} lines in csv file.".format(len(data)))
            row_list = []
            for i in range(0, len(data)):
                temp_row = NAPRow(data[i])
                temp_row.generate_data()
                row_list.append(temp_row)

        return row_list


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
    def groupInvoicesBy(self, bySAR=None, gpOutput='r', excelOutput=True):
        pass