__author__ = 'nabeelh-dev'

from naptax.models.NAPcollection import NAPcollection


test_list = ['data/test_NAPGLDATA/',
             'data/test_NAPGLDATA/ADLT0718-0818.csv']
def run():
    for test_fp in test_list[1:]:
        test_path_collection = NAPcollection(test_fp)
        print(test_path_collection.filepath)
        print(test_path_collection.getGLCodes())
        #print(test_path_collection.getRegionCodes())
        #print(test_path_collection.getAreaCodes())
        #print(test_path_collection.getSectionCodes())
        #print(test_path_collection.getTRXDateRange())
        #print(test_path_collection.getPostingDateRange())
        #print(test_path_collection.getFileSources())

    test_invoice = test_path_collection.naprows[1]
    print(test_invoice.invoice_data['glAcct'])
    test_invoice.invoice_data = {
                                'glAcct' : 9999
                                }
    print(test_invoice.invoice_data['glAcct'])
    #print(test_path_collection.naprows[0].source_metainfo)

if __name__ == "__main__":
    run()



