#!/usr/bin/env python

import sys
from PyQt4 import QtGui
from archydro_ts.processors import processors


class TimeSeriesGUI(QtGui.QWidget):

    COLS = [20, 150, 300]
    processors_dict = None
    data = {
        'processor': None,
        'source_data': '/home/rohan/workspace/btp/data/imd.xls',
        'stations_data': '/home/rohan/workspace/btp/data/storg.dbf',
        'save_file': ''
    }

    data_files = {}

    def __init__(self, app):
        super(TimeSeriesGUI, self).__init__()
        self.app = app
        self.initUI()

    def get_processors(self):
        if self.processors_dict:
            return self.processors_dict

        processors_dict  = {}
        for processor in processors:
            processors_dict[processor[2]] = processor[1]

        self.processors_dict = processors_dict
        return processors_dict

    def set_processor(self, title):
        self.data['processor'] = self.get_processors().get(str(title))

    def source_data_dialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,
                                                  'Open Source Data File')
        if fname:
            self.source_data.setText(fname)
            self.data['source_data'] = str(fname)

    def stations_data_dialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,
                                                  'Open Stations Data File',
                                                  '', '*.dbf')
        if fname:
            self.stations_data.setText(fname)
            self.data['stations_data'] = str(fname)

    def save_file_dialog(self):
        initial = ''
        if self.data['source_data']:
            initial = '.'.join(self.data['source_data'].split('.')[0:-1]+['dbf'])
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Timseries As',
                                                  initial, '*.dbf')
        if fname:
            self.save_file.setText(fname)
            self.data['save_file'] = str(fname)

    def process_submit(self):
        self.result_label.setText('Processing...')
        QtGui.QApplication.processEvents()
        self.process_data()

    def process_data(self):
        processor = self.data['processor']
        source_data = self.data['source_data']
        stations_data = self.data['stations_data']
        save_file = self.data['save_file']

        if processor and source_data and stations_data and save_file:
            try:
                instance = processor(stations_data, source_data)
                instance.get_timeseries()
                instance.create_timeseries_dbase(save_file)
                self.result_label.setText('Successfull!')
            except:
                self.result_label.setText('Processing Error!')
                raise
        else:
            self.result_label.setText('Incomplete Info')

    def initUI(self):

        #Combo for data processors
        combo_label = QtGui.QLabel(self)
        combo_label.setText('Data Processor:')
        combo = QtGui.QComboBox(self)
        processor_set = False

        for processor in self.get_processors():
            if not processor_set:
                self.set_processor(processor)
                processor_set = True

            combo.addItem(processor)
        combo.activated[str].connect(self.set_processor)
        combo.resize(combo.sizeHint())

        #Source Data
        source_data_label = QtGui.QLabel(self)
        source_data_label.setText('Source Data File:')
        source_data = QtGui.QLineEdit(self)
        source_data_button = QtGui.QPushButton('Browse', self)
        source_data_button.clicked.connect(self.source_data_dialog)

        #Source Data
        stations_data_label = QtGui.QLabel(self)
        stations_data_label.setText('Stations Data File:')
        stations_data = QtGui.QLineEdit(self)
        stations_data_button = QtGui.QPushButton('Browse', self)
        stations_data_button.clicked.connect(self.stations_data_dialog)

        #Save file name
        save_file_label = QtGui.QLabel(self)
        save_file_label.setText('Save to file:')
        save_file = QtGui.QLineEdit(self)
        save_file_button = QtGui.QPushButton('Browse', self)
        save_file_button.clicked.connect(self.save_file_dialog)


        #Status
        result_label = QtGui.QLabel(self)
        result_label.setUpdatesEnabled(True)
        result_label.setText(" "*200)
        output_file_label = QtGui.QLabel(self)
        output_file_label.setText(" "*200)

        #Submit button
        btn = QtGui.QPushButton('Process', self)
        btn.clicked.connect(self.process_submit)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())

        combo_label.move(self.COLS[0], 20)
        combo.move(self.COLS[1], 20)

        source_data_label.move(self.COLS[0], 60)
        source_data.move(self.COLS[1], 60)
        source_data_button.move(self.COLS[2], 60)

        stations_data_label.move(self.COLS[0], 100)
        stations_data.move(self.COLS[1], 100)
        stations_data_button.move(self.COLS[2], 100)

        save_file_label.move(self.COLS[0], 140)
        save_file.move(self.COLS[1], 140)
        save_file_button.move(self.COLS[2], 140)

        btn.move(self.COLS[0], 180)
        result_label.move(self.COLS[1], 180)

        self.combo = combo
        self.source_data = source_data
        self.stations_data = stations_data
        self.save_file = save_file
        self.result_label = result_label

        self.setGeometry(50, 50, 450, 250)
        self.setWindowTitle('ArcHydro Timeseries Creator')
        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    tseries_gui = TimeSeriesGUI(app)
    sys.exit(app.exec_())
    del tseries_gui

if __name__ == '__main__':
    main()
