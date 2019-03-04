__author__ = 'nabeelh-dev'

import os
import csv


class TaxRates(object):
    """
    Data model that will load up static tax csv file data into a dict.
    Dict will be contained in self.tax_rates.
    Will be able to query by zipcode.

    e.g
    TaxRates.query_by_zipcode('99501')
    >>>{
        "region_name": "ALASKA STATE",
        "state_rate" : 0.000000,
        "est_combined_rate": 0.000000,
        "est_country_rate": 0.000000,
        "est_city_rate": 0.000000,
        "est_special_rate": 0.000000,
        "risk_level": 1,
        "zipcode": "99501",
        "state": "AK"
        }
    """
    def __init__(self, csv_path):
        self.filepath = csv_path
        self.tax_rates = self.parse_csv()

    def parse_csv(self):
        """
        Takes str value for directory stored in self.filepath and will process
        all tax rate csv files within. Will return a dict that will be set to
        TaxRates objects self.tax_rates so we can query by zipcode.
        self.tax_rates will contain a dict that has two main keys:
        'state_tax_rates': stores all State -> Zipcode -> TaxRates dict
        'zipcode_to_state': will be a list of lists, sorted by all states zipcode ranges

        zipcode_to_states list will be used for fast querying when looking for zipcodes tax rates.
        It will quickly indicate the state we will need to look inside to find the zipcode tax rates,
        isntead of looping through state_tax_rates dict which would be inefficient.

        CSV file names to parse are in this format: TAXRATES_ZIP5_AK201901.csv
        We will want to extract the state name from the filename.

        e.g states_tax_rates:
        {
            'state_tax_rates': {
                                'AK': {
                                        '99501': {
                                                "region_name": "ALASKA STATE",
                                                "state_rate" : 0.000000,
                                                "est_combined_rate": 0.000000,
                                                "est_country_rate": 0.000000,
                                                "est_city_rate": 0.000000,
                                                "est_special_rate": 0.000000,
                                                "risk_level": 1
                                                },
                                        },
                                },
            'zipcode_to_state': {
                                '82397': 'WY',
                                '83414': 'WY',
                                '89001': 'NV',
                                '89883': 'NV',
                                '99501': 'AK',
                                '99950': 'AK',
                                }
        }

        :param: self.filepath: str
        :return: states_tax_rates: dict
        """
        states_tax_rates = dict()
        zipcode_to_state = dict()

        # directory input, process all .csv contained within directory
        dirpath = os.path.dirname(__file__)
        csv_dp = os.path.join(dirpath, "../../" + self.filepath)
        for filename in os.listdir(csv_dp):
            # splits filename to identify state: TAXRATES_ZIP5_AK201901.csv
            csv_state_abbr = filename.split("ZIP5_")[1][:2]
            if filename.endswith(".csv"):
                filepath = os.path.join(csv_dp, filename)
                # states_tax_rates[csv_state_abbrevistion] = TaxRates._parse_single_csv(filepath)
                csv_tax_rates = TaxRates._parse_single_csv(filepath)
                # Assigns dict of tax rates by zipcode to state abbreviation
                states_tax_rates[csv_state_abbr] = csv_tax_rates['zipcode_rates']

        # Fill up zipcode_to_state dict
        for state, zipcode_tax_rates in states_tax_rates.items():
            for zipcode, tax_rates in zipcode_tax_rates.items():
                zipcode_to_state[zipcode] = state

        print("Zipcode Tax Rates loaded successfully.")
        return {
                "state_tax_rates": states_tax_rates,
                "zipcode_to_state": zipcode_to_state
                }

    @staticmethod
    def _parse_single_csv(csv_fp):
        """
        Parses csv at file path. Collects and stores all zipcode data as a dict.
        When being read by csv.reader, each row will be a list as follows:
        ['WY', '83118', 'LINCOLN COUNTY', '0.040000', '0.050000', '0.010000', '0', '0', '1']
        Data will be converted to a dict.

        Will also keep track of zipcode values and return
        the 'lowest' zipcode value and highest in the csv file, under the key 'low_high_zipcode'.
        This will be used to help to make query_by_zipcode class function perform faster.
        Will take advantage of the fact that the csv files are all in zipcode value descending order.

        e.g
        {
            'zipcode_rates' : {
                                '83118': {
                                        "region_name": "LINCOLN COUNTY",
                                        "state_rate" : 0.040000,
                                        "est_combined_rate": 0.050000,
                                        "est_country_rate": 0.010000,
                                        "est_city_rate": 0.000000,
                                        "est_special_rate": 0.000000,
                                        "risk_level": 1
                                        },
                                },
            'low_high_zipcode' : [82001, 83414]

        :param csv_fp: os path object
        :return: state_dict: dict
        """
        zipcode_rates = dict()
        with open(csv_fp) as csv_file:
            #print("Opened Tax CSV Successfully: {}".format(str(csv_fp)))
            csv_reader = csv.reader(csv_file)
            # Skip the first 6 line of csv file due to header
            for i in range(0, 1, 1):
                next(csv_reader, None)

            for zipcode_tax in csv_reader:
                zipcode = zipcode_tax[1]
                region_name = zipcode_tax[2]
                state_rate = float(zipcode_tax[3])
                est_combined_rate = float(zipcode_tax[4])
                est_country_rate = float(zipcode_tax[5])
                est_city_rate = float(zipcode_tax[6])
                est_special_rate = float(zipcode_tax[7])
                risk_level = int(zipcode_tax[8])

                zipcode_rates[zipcode] = {
                                        "region_name": region_name,
                                        "state_rate" : state_rate,
                                        "est_combined_rate": est_combined_rate,
                                        "est_country_rate": est_country_rate,
                                        "est_city_rate": est_city_rate,
                                        "est_special_rate": est_special_rate,
                                        "risk_level": risk_level
                                        }

            """
            # Below I am taking advantage of the order of the columns in the csv file.
            # Ensure the colnames and functions you want to apply to them are in order
            # in the zipcode_cols_config list below.
            # Current Order in ZIP files:-
                # State,ZipCode,TaxRegionName,StateRate,EstimatedCombinedRate,
                # EstimatedCountyRate,EstimatedCityRate,EstimatedSpecialRate,RiskLevel
            for zipcode_tax in csv_reader:
                # Add some validation check for each row: maybe check for len?
                # (col_name, col_function())
                zipcode_cols_config = [
                                        ["zipcode"], [lambda x: x],
                                        ["region_name"], [lambda x: x],
                                        ["state_rate"], [float()],
                                        ["est_combined_rate"], [float],
                                        ["est_country_rate"], [float],
                                        ["est_city_rate"], [float],
                                        ["est_special_rate"], [float],
                                        ["risk level"], [int]
                                        ]
                # zip(*[list of tuples]) = actually unzips list of tuples.
                # Apply contents to row starting from 2 because we are already using State & Zip
                
                for i, csv_data in enumerate(zipcode_tax[2:]):
                    zipcode_rates[zipcode_cols_config[i]] = zipcode_cols_config[i](csv_data)
                    
                or
                    
                for csv_col in zipcode_tax[2:]:
                    print(csv_col)
                    for col_config in zipcode_cols_config:
                        print(col_config)
                        for col_name, col_func in zip(*col_config):
                            print(col_name)
                            zipcode_rates[col_name] =  col_func(csv_col) if col_config[1] else csv_col

                """

        return {
                'zipcode_rates': zipcode_rates
                }

    def query_by_zipcode(self, zipcode_str):
        """
        Given a zipcode string, retrieve tax rates for that zipcode.
        First accesses 'zipcodes_to_state' dict contained in self.tax_rates to get
        the State the zipcode is in.
        If zipcode_str does not exist, then print error and return None.

        If it exists then uses State key and Zipcode key to obtain correct tax rates from
        'state_tax_rates' dict in self.tax_rates

        :param zipcode_str: str
        :return: zipcode_tax_rates: dict
        """

        # dict get method returns None if key is not found
        query_state = self.tax_rates['zipcode_to_state'].get(zipcode_str)
        if query_state is None:
            print("{} - zipcode not found!".format(zipcode_str))
            return None
        query_results = self.tax_rates['state_tax_rates'][query_state][zipcode_str]
        query_results['zipcode'] = zipcode_str
        query_results['state'] = str(query_state)
        return query_results



