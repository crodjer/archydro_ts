import base
import xlrd

class XLTimeseries(base.BaseTimeseries):

    book = None

    def __init__(self, feature_id_source, data_source):
        super(XLTimeseries, self).__init__(feature_id_source, data_source)
        self.book = xlrd.open_workbook(self.data_source)

    def process_sheet(self, sheet):
        raise NotImplementedError('Data from source of this type cannot be \
                                   processed')

    def _get_sheets(self):
        return self.book.sheets()[1:]

    def process_source(self):
        source_data = {}
        unprocessed_sheets = []

        for (index, sheet) in enumerate(self._get_sheets()):
            try:
                feature_data = self.process_sheet(sheet)
                source_data[sheet.name.lower()] = feature_data

            except (ValueError, UnboundLocalError):
                unprocessed_sheets.append(sheet.name)

        self.data = source_data.items()
        return self.data
