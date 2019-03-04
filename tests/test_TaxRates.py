__author__ = 'nabeelh-dev'

from naptax.analyze.TaxRates import TaxRates


test_list = ['data/TAXRATES_ZIP5/']

def run():
    for test_fp in test_list:
        test_tax_rates = TaxRates(test_fp)
        #print(test_tax_rates.tax_rates['zipcode_to_state'])

        zipcodes_list = ['90247', '90210', '99901', 'invalid']
        for zipcode in zipcodes_list:
            zipcode_query = test_tax_rates.query_by_zipcode(zipcode)
            if zipcode_query is not None:
                print(zipcode_query['zipcode'], zipcode_query['region_name'], zipcode_query['state'])


if __name__ == "__main__":
    run()