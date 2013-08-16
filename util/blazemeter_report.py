"""
Script to generate report from BlazeMeter load test data.

Usage:

    python blazemeter_report.py data.csv


Outputs:

    * latency_graph.png (hits/sec versus latency)
    * error_graph.png (hits/sec versus error responses per sec)
    * 50th, 90th, and 99th percentile response times,
      excluding data points with > 1% error rates
"""

import sys
import csv
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt


USAGE = "python blazemeter_report.py data.csv"

# Colors of lines in the graph
COLORS = ['#b72e3e', '#3e94d1']

class LoadData(object):
    """
    Representation of BlazeMeter load test data.
    """

    # Dict mapping names to columns in the CSV
    INDEX_DICT = {
        'label': 0,
        'datetime': 2,
        'latency': 3,
        'response_time': 4,
        'hits_per_sec': 5,
        'num_200_resp': 7,
        'num_err_resp': 9
    }

    def __init__(self, csv_path):
        """
        Load the CSV file at `csv_path`.
        """
        self._data = []
        self._load_csv_data(csv_path)

    def minute_series(self):
        """
        Return a list of minutes in the test,
        starting at minute 0.
        """
        return [minute for minute in range(0,len(self._data))]

    def latency_series(self):
        """
        Return a list of reported latencies (ms)
        for each minute of the test.
        """
        return [
            self._float(item['latency'])
            for item in self._data
        ]

    def num_requests_series(self):
        """
        Return list of total num req/min for each
        minute of the test.
        """
        return [
            self._float(item['num_200_resp']) + self._float(item['num_err_resp'])
            for item in self._data
        ]

    def error_series(self):
        """
        Return the error rate (%) for each minute of the test.
        """
        return [
            self._error_rate(item)
            for item in self._data
        ]

    def resp_time_percentile(self, percentile):
        """
        Return nth percentile response times,
        filtering out minutes with error rates > 1%.

        Returns None if no times have a low enough
        error rate.
        """
        resp_time_array = np.array([
            self._float(item['response_time'])
            for item in self._data
            if self._error_rate(item) < 0.01
        ])

        if len(resp_time_array) < 1:
            return None
        else:
            return np.percentile(resp_time_array, percentile)

    def _load_csv_data(self, csv_path):
        """
        Load the CSV data from BlazeMeter, using only
        info labelled "ALL"
        """
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self._parse_row(row)

    def _parse_row(self, row):
        """
        Parse a row in the BlazeMeter CSV file,
        filtering out anything that isn't labelled "ALL"
        """
        if self._row_data(row, 'label') == 'ALL':

            data_item = {
                key: self._row_data(row, key)
                for key in self.INDEX_DICT.keys()
            }

            self._data.append(data_item)

    def _row_data(self, row, index_name):
        return row[self.INDEX_DICT[index_name]]

    def _float(self, val):
        """
        Safely handle conversion to float for
        empty strings and None values.
        """
        if val != '' and val is not None:
            return float(val)
        else:
            return 0

    def _error_rate(self, data_item):
        return self._float(data_item['num_err_resp']) / \
                (self._float(data_item['num_200_resp']) + \
                self._float(data_item['num_err_resp']))

def main(args):
    if len(args) < 2:
        print USAGE
        exit(1)

    # First arg is csv file path
    load_data = LoadData(args[1])

    # Generate the data
    create_latency_graph(load_data)
    create_error_graph(load_data)
    create_resp_percentile_report(load_data)


def create_graph(title,
                 indep_label, indep_series,
                 dep_label_1, dep_series_1,
                 dep_label_2, dep_series_2,
                 output_file_name):
    """
    Plot two series on a graph.
    """
    # Plot two series on the graph
    fig, axis_1 = plt.subplots()

    # Set the title
    fig.suptitle(title, fontsize=20)

    # Plot the first series
    axis_1.plot(indep_series, dep_series_1, color=COLORS[0])
    axis_1.set_xlabel(indep_label)
    axis_1.set_ylabel(dep_label_1, color=COLORS[0])
    for tick in axis_1.get_yticklabels():
        tick.set_color(COLORS[0])

    # Plot the second series
    axis_2 = axis_1.twinx()
    axis_2.plot(indep_series, dep_series_2, color=COLORS[1])
    axis_2.set_ylabel(dep_label_2, color=COLORS[1])
    for tick in axis_2.get_yticklabels():
        tick.set_color(COLORS[1])

    # Output the figure
    plt.grid(True)
    print "Creating {}".format(output_file_name)
    plt.savefig(output_file_name, dpi=200, bbox_inches='tight')



def create_latency_graph(load_data):
    create_graph('Latency', 'Minutes', load_data.minute_series(),
                 'Latency (ms)', load_data.latency_series(),
                 'Num Requests Per Minute', load_data.num_requests_series(),
                 'latency.png')


def create_error_graph(load_data):
    create_graph('Error Rate', 'Minutes', load_data.minute_series(),
                 'Error rate (%)', load_data.error_series(),
                 'Num Requests Per Minute', load_data.num_requests_series(),
                 'errors.png')


def create_resp_percentile_report(load_data):

    print ("Response time (50th percentile): {} ms".format(
        load_data.resp_time_percentile(50)))
    print ("Response time (90th percentile): {} ms".format(
        load_data.resp_time_percentile(90)))
    print ("Response time (99th percentile): {} ms".format(
        load_data.resp_time_percentile(99)))


if __name__ == "__main__":
    main(sys.argv)
