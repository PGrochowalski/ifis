import csv
import pickle as pk
import pandas as pd
from _warnings import warn
import random


class ImportData:

    @staticmethod
    def read_raw_data_pickle_file(data_file_name, all_arg, *args):
        """
        :param data_file_name: name of pickle file that contains data
        :param all_arg: if True all arg will be read, otherwise only selected one
        :param args: names of attribute that will be read from pickle file
        :return: function will return [[attributes], data dictionary]
        """

        attributes = []
        features_in = open(data_file_name, 'rb')
        features = pd.read_pickle(features_in)
        # features = pk.load(features_in) # for pandas 1.5.3 or lower
        del features_in
        raw_data = {}
        first_key = list(features.keys())[0]

        for k in features.keys():
            all_frames = features[k]
            data_read_table = []
            if all_arg:
                for i in range(0, len(features[first_key].keys())):
                    data_read_table.append(all_frames.get(features[first_key].keys()[i]))
                raw_data[k] = data_read_table
                attributes = list(features[first_key].keys())
            else:
                for i in range(0, len(args)):
                    data_read_table.append(all_frames.get(args[i]))
                raw_data[k] = data_read_table
                attributes = list(args)

        return [attributes, raw_data]

    @staticmethod
    def convert_data_dict2table(*args):
        """
        :param args: data set prepared in function read_raw_data_pickle_file
        :return: concatenated array
        """

        all_arg = []
        for key in args[0].keys():
            # check if all column data are the same size
            minimum = len(args[0][key][0])
            inconsistency_key = None
            for arg in args:
                if minimum != len(arg[key][0]):
                    inconsistency_key = key
                    if minimum > len(arg[key][0]):
                        minimum = len(arg[key][0])
            if inconsistency_key is not None:
                warning_message = "\ninconsistency found in key: " + inconsistency_key
                warn(warning_message)
                inconsistency_key = None

            for i in range(1, minimum+1):
                line = []
                for arg in args:
                    for element in range(0, len(arg[key])):
                        line.append(arg[key][element][i])
                all_arg.append(line)

        return all_arg

    @staticmethod
    def cut_data(data, percent, no_class_column=None):
        """
        :param data: data array prepared by convert_data_dict2table
        :param percent: percent of data that will be cut
        :param no_class_column: number of class column if contained
        :return: data array with cut data
        """

        cut_record_lines = []
        no_column = len(data[0])
        data_to_cut = len(data) * (percent / 100)
        i = 0
        while i < int(data_to_cut):
            record = random.randint(0, len(data) - 1)
            if record not in cut_record_lines:
                lottery = random.randint(0, no_column - 1)
                if lottery != no_class_column:
                    i += 1
                    data[record][lottery] = [0, 1]
                    cut_record_lines.append(record)

        return data

    @staticmethod
    def is_float(s):
        """
        :param s: string value to check if it's float
        :return: True if value is float, False otherwise
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def read_data_csv(data_file_name, all_arg, *args):
        """
        :param data_file_name: path to file that will be read
        :param all_arg: set True to read all arguments, to choose some of them set False
        :param args: if all_arg is False, set names of attributes to red from file
        :return: Data Array
        """

        with open(data_file_name, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            all_data = []
            col_search = csvreader.__next__()
            if len(col_search) * 2 != len(csvreader.__next__()):
                warn("Doubled number of attributes is not the same as number of columns")
            if all_arg:
                for row in csvreader:
                    row_data = []
                    for col in range(len(col_search)):
                        interval = []

                        if ImportData.is_float(row[col * 2]):
                            interval.append(float(row[col * 2]))
                        else:
                            interval.append(row[col * 2])
                        if ImportData.is_float(row[col * 2 + 1]):
                            interval.append(float(row[col * 2 + 1]))
                        else:
                            interval.append(row[col * 2 + 1])
                        row_data.append(interval)
                    all_data.append(row_data)
                all_data.insert(0, col_search)
            else:
                no_col = []

                for arg in args:
                    if col_search.__contains__(arg):
                        no_col.append(col_search.index(arg))
                print(no_col)
                for row in csvreader:
                    row_data = []
                    for col in no_col:
                        interval = []
                        if ImportData.is_float(row[col * 2]):
                            interval.append(float(row[col * 2]))
                        else:
                            interval.append(row[col * 2])

                        if ImportData.is_float(row[col * 2 + 1]):
                            interval.append(float(row[col * 2 + 1]))
                        else:
                            interval.append(row[col * 2 + 1])

                        row_data.append(interval)

                    all_data.append(row_data)
                all_data.insert(0, list(args))
            attributes = []
            if all_arg:
                for arg in col_search:
                    attributes.append(arg)
            else:
                attributes = list(args)

            all_data = all_data[1:]
            return [[attributes], all_data]
