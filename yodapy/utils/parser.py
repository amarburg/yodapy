# -*- coding: utf-8 -*-

from __future__ import (division,
                        absolute_import,
                        print_function,
                        unicode_literals)

import datetime

import netCDF4 as nc

from siphon.catalog import TDSCatalog


def get_nc_urls(thredds_url, download=False):
    urltype = 'OPENDAP'
    if download:
        urltype = 'HTTPServer'
    caturl = thredds_url.replace('.html', '.xml')
    cat = TDSCatalog(caturl)
    ncfiles = list(filter(lambda d: not any(w in d.name for w in ['json', 'txt', 'ncml']),  # noqa
                          [cat.datasets[i] for i, d in enumerate(cat.datasets)]))  # noqa
    dataset_urls = [d.access_urls[urltype] for d in ncfiles]
    return dataset_urls


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds() * 1000)


def datetime_to_string(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def seconds_to_date(num):
    return nc.num2date(num, 'seconds since 1900-01-01')


def get_midnight(dt):
    nextday = dt + datetime.timedelta(1)
    time_labels = ('hour', 'minute', 'second', 'microsecond')
    time_list = nextday.hour, nextday.minute, nextday.second, nextday.microsecond  # noqa
    zeroed = tuple(map(lambda x: 0 if x > 0 else x, time_list))
    return nextday.replace(**dict(zip(time_labels, zeroed)))


def ooi_instrument_reference_designator(reference_designator):
    """
    Parses reference designator into a dictionary containing subsite, node,
    and sensor.

    Args:
        reference_designator (str): OOI Instrument Reference Designator

    Returns:
        Dictionary of the parsed reference designator
    """

    keys = ['subsite', 'node', 'sensor']
    val = reference_designator.split('-')
    values = val[:-2] + ['-'.join(val[-2:])]
    return dict(zip(keys, values))


def build_url(*args):
    return '/'.join(args)
