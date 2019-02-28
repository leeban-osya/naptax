from naptax.models.NAPCollection import NAPCollection

test_fp = 'data/test_NAPGLDATA/CORE0718-0818.csv'

def run():
    test_collection = NAPCollection(test_fp)

    # print(test.getGLCodes())
    # print(test.getRegionCodes())
    # print(test.getAreaCodes())
    # print(test.getSectionCodes())

    print(test_collection.getTRXDateRange())
    print(test_collection.getPostingDateRange())









if __name__ == "__main__":
    run()



