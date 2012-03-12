from calendar import monthrange
from datetime import date

from ..lib import xlspreadsheet

class Timeseries(xlspreadsheet.XLTimeseries):

    tseries_type_id = 4
    title = 'MC Bhubhaneshwar 08 and up'
    feature_id_headers = ('STATION', 'HYDROID')
    start_row = 26

    def process_row(self, sheet, values):
        data = {} 

        year_cell = int(values[0])
        if year_cell > 20:
            year = 1900 + year_cell
        else:
            year = 2000 + year_cell

        month = int(values[1])
        month_half = int(values[2]) 
        station = values[23].lower()

        if month_half == 1:
            start_date = 1
            end_date = 16
        else:
            start_date = 17
            end_date = monthrange(year, month)[1]

        for i, cur_date in enumerate(xrange(start_date, end_date+1)):
            value = values[i+3]

            if value:
                data[date(year, month, cur_date)] = float(value)

        return (station, data)


    def process_sheet(self, sheet):
        '''
        Takes in an xlrd document and the sheet index to convert the rainfall
        data to a format further usable in python scripts.  Returns a dictionary
        with dates (in datetime library date type), sorted by date as keys and
        the rainfall as values
        '''

        # Stores data as key value pairs
        data = {}

        for index in xrange(self.start_row, sheet.nrows): 
            values = sheet.row_values(index)[5:29]
            if values[0] and values[1] and values[2]:
                station, station_data = self.process_row(sheet, values)

            if station in data:
                data[station].update(station_data)
            else:
                data[station] = station_data

        for station in data:
            data[station] = sorted(data[station].items())

        return data

    def process_source(self):
        source_data = self.process_sheet(self.book.sheets()[0])
        self.data = source_data.items()

        return self.data
