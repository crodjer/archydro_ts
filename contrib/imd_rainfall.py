from datetime import date
from time import strptime

from ..lib import xlspreadsheet

class Timeseries(xlspreadsheet.XLTimeseries):

    tseries_type_id = 1
    title = 'IMD Rainfall'
    feature_id_headers = ('STATION', 'HYDROID')

    def process_sheet(self, sheet):
        '''
        Takes in an xlrd document and the sheet index to convert the imd
        rainfall data to a format further usable in python scripts.
        Returns a dictionary with dates (in datetime library date type), sorted
        by date as keys and the rainfall as values
        '''

        # Stores data as key value pairs
        data = {}
        # List of years for which data can be present in the sheet
        years = []
        # The column in which first year is present,
        # for use to start the data parsing from this index
        year_start_column = 0
        for (index, cell) in enumerate(sheet.row_types(0)):
            if not (cell is 0 or cell is 6):
                year_start_column = index
                break

        for year in sheet.row_values(0)[year_start_column:]:
            years.append(int(year))

        for i in xrange(sheet.nrows):
            row = sheet.row_values(i)
            if row[1]:
                if row[0]:
                    # A new month starts here, update the current month
                    try:
                        current_month = strptime(row[0], '%b').tm_mon
                    except ValueError:
                        current_month = strptime(row[0], '%B').tm_mon
                for (value, year) in zip(row[year_start_column:], years):
                    if type(value) in (int, float):
                        # Add the data to data dictionary with the date as a key
                        data[date(year, int(current_month), int(row[1]))]=value

        return sorted(data.items())
