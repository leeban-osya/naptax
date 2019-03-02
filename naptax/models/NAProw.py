__author__ = 'nblh'

import json

class NAProw(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.glacct = None
        self.glacctdesc = None
        self.refnum = None
        self.trxtype = None
        self.trxdate = None
        self.gldate = None
        self.trxdesc = None
        self.paidtorcvd = None
        self.trxamt = None
        self.debitamt = None
        self.creditamt = None
        self.section = None
        self.area = None
        self.region = None

    def __repr__(self):
        return "<Invoice: SAR: {}-{}-{} GL Acct: {}>".format(self.section,
                                                             self.area,
                                                             self.region,
                                                             self.glacct)

    def generate_data(self):
        for k,v in self.raw_data.items():
            if k == 'Segment3':
                self.section = v
            if k == 'Segment4':
                self.area = v
            if k == 'Segment5':
                self.region = v
            if k == 'Account Description':
                self.glacctdesc = v
            if k == 'Record Type::Number':
                self.refnum = v
            if k == 'CM Trx Type':
                self.trxtype = v
            if k == 'TRX Timestamp Date':
                self.trxdate = v
            if k == 'GL Posting Date':
                self.gldate = v
            if k == 'Description':
                self.trxdesc = v
            if k == 'Main Account Segment':
                self.glacct = v
            if k == 'PaidToRcvd':
                self.paidtorcvd = v
            if k == 'TRX Amount':
                self.trxamt = v
            if k == 'Originating Debit Amount':
                self.debitamt = v
            if k == 'Originating Credit Amount':
                self.creditamt = v

    def toJSON(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)

