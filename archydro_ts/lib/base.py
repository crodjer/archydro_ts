from dbfpy import dbf

class BaseTimeseries(object):

    feature_id_source = None
    data_source = None
    data = None
    feature_ids = None
    unprocessed_features = []
    tseries_type_id = None
    tseries = None

    feature_id_headers = ('STATION', 'HYDROID')

    def __init__(self, feature_id_source, data_source):
        self.feature_id_source = feature_id_source
        self.data_source = data_source

    @classmethod
    def get_title(self):
        return self.title

    def get_feature_ids(self):
        if self.feature_ids:
            return self.feature_ids

        db = dbf.Dbf(self.feature_id_source)
        key_header, value_header = self.feature_id_headers
        feature_ids = {}
        for rec in db:
            feature_ids[rec[key_header].lower().strip()] = rec[value_header]

        return feature_ids

    def process_source(self):
        raise NotImplementedError('Data from source of this type cannot be \
            processed')

    def _get_feature_tseries(self, feature_data, feature_id):
        series = []
        for date, value in feature_data:
            date_data = (
                feature_id,
                self._get_tseries_type_id(),
                date,
                value
            )
            series.append(date_data)

        return series

    def _get_tseries_type_id(self):
        if self.tseries_type_id != None:
            return self.tseries_type_id
        else:
            raise NotImplementedError('Module for processing from this source \
                is not implemented properly')

    def get_data(self):
        if self.data:
            return self.data

        self.data = self.process_source()
        return self.data

    def get_timeseries(self):

        if self.tseries:
            return self.tseries

        feature_ids = self.get_feature_ids()
        tseries = []
        data = self.get_data()

        for feature, feature_data in data:
            feature_id = feature_ids.get(feature, '')
            if feature_id:
                tseries += self._get_feature_tseries(feature_data, feature_id)
            else:
                self.unprocessed_features.append(feature)

        self.tseries = tseries
        return tseries

    def create_timeseries_dbase(self, filename):
        tseries = self.get_timeseries()

        db = dbf.Dbf(filename, new=True)
        db.addField(
            ('FEATUREID', 'N', 3, 0),
            ('TSTYPEID', 'N', 1, 0),
            ('TSDATETIME', 'D'),
            ('TSVALUE', 'N', 10, 2),
        )

        for datum in tseries:
            rec = db.newRecord()
            rec["FEATUREID"], rec["TSTYPEID"], rec["TSDATETIME"], rec["TSVALUE"] = datum
            rec.store()
        db.close()
