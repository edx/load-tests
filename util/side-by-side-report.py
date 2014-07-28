"""
This script accepts a list of blazemeter test results (in JSON format) and produces
a csv on stdout with statistics side-by-side, making it a bit easier to compare the
results across a series tests.

Usage example:

> python side-by-side-report.py baseline.json branch-1.json branch-2.json > report.csv

"""
from collections import namedtuple
import csv
from datetime import datetime
import json
import sys

Stat = namedtuple('Stat', 'std average min max samples median percentile90 percentile99 errorPercentage hits kbs n')

CSV_STATS = 'samples median average min percentile90 percentile99 max errorPercentage kbs'.split(' ')

NON_ERROR_INDICATORS = set([
    "200",
    "Latency",
    "Response Time",
    "Hits/s",
    "Max Users",
    "Active Users",
    "Errors",
    "Embedded Resources",
    "KB/s"
])

def _merge(*lists):
    """
    merge multiple lists to a single list of unique values
    """
    return list(set([v for list_ in lists for v in list_]))

class Test(object):

    @classmethod
    def from_json_file(cls, f, name=None):
        d = json.load(f)
        name = getattr(f, 'name', None)
        if name and name.lower().endswith(".json"):
            name = name[:-5]
        if not name:
            name = '?'
        start_dt = datetime.fromtimestamp(float(d['timestamps'][0])/1000)
        end_dt = datetime.fromtimestamp(float(d['timestamps'][-1])/1000)
        stats = {}
        for k, v in d['aggregate'].iteritems():
            stats[k] = Stat(*[v[n] for n in Stat._fields])
        errors = {}
        for k, v in d['results'].iteritems():
            for k2, v2 in v['intervals'].iteritems():
                indicators = set(v2['indicators'].keys()) - NON_ERROR_INDICATORS
                for indicator in indicators:
                    errors.setdefault(k, {})
                    errors[k].setdefault(indicator, 0)
                    errors[k][indicator] += int(v2['indicators'][indicator]['value'])
        return cls(name, start_dt, end_dt, stats, errors)

    def __init__(self, name, start_dt, end_dt, stats, errors):
        self.name = name
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.stats = stats
        self.errors = errors

    @property
    def stats_keys(self):
        return self.stats.keys()

    @property
    def error_keys(self):
        return _merge(*[v.keys() for v in self.errors.values()])

    @property
    def duration(self):
        return (self.end_dt - self.start_dt).seconds

def main(files):
    if not files:
        raise Exception("no files to process")
    # assume every input file is a json file.
    tests = [Test.from_json_file(f) for f in files]
    make_csv(sys.stdout, tests)

def make_csv(out, tests):
    writer = csv.writer(out)
    writer.writerow(['test name', ''] + [t.name for t in tests])
    writer.writerow(['test date', ''] + [t.start_dt.strftime("%Y-%m-%d %H:%M:%S") for t in tests])
    writer.writerow(['test duration', ''] + ['{:.2}h'.format(t.duration/3600.0) for t in tests])
    writer.writerow([''] * (len(tests)+2))

    keys = sorted(_merge(*[t.stats_keys for t in tests]))
    for key in keys:
        for stat in CSV_STATS:
            writer.writerow([key, stat] + [getattr(test.stats.get(key), stat, None) for test in tests])
        for error in _merge(*[t.errors.get(key, {}).keys() for t in tests]):
            writer.writerow([key, 'error: {}'.format(error)] + [test.errors.get(key, {}).get(error, 0) for test in tests])
        writer.writerow([''] * (len(tests)+2))


if __name__=='__main__':
    main([open(filename, 'rb') for filename in sys.argv[1:]])
