#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# =============================================================================
# Import modules
# =============================================================================
import psutil
import os
import sys
import numpy as np
import xarray as xr
import pandas as pd
import calendar as cld
import proplot as plot
from cartopy.util import add_cyclic_point


# =============================================================================
# Basic functions
# =============================================================================
def check_python_version():
    print(sys.version)

def check_virtual_memory():
    # https://psutil.readthedocs.io/en/latest/#psutil.virtual_memory
    values = psutil.virtual_memory()
    print("Virtual memory usage - " +
          "total: " + str(get_human_readable_size(values.total)) + " / " +
          "available: " + str(get_human_readable_size(values.available)) + " / " +
          "percent used: " + str(values.percent) + " %"
          )

def get_human_readable_size(num):
    # https://stackoverflow.com/questions/21792655/psutil-virtual-memory-units-of-measurement
    exp_str = [ (0, 'B'), (10, 'KB'),(20, 'MB'),(30, 'GB'),(40, 'TB'), (50, 'PB'),]               
    i = 0
    while i+1 < len(exp_str) and num >= (2 ** exp_str[i+1][0]):
        i += 1
        rounded_val = round(float(num) / 2 ** exp_str[i][0], 2)
    return '%s %s' % (int(rounded_val), exp_str[i][1])


# =============================================================================
# Compute monthly weighted data
# =============================================================================
# http://xarray.pydata.org/en/stable/examples/monthly-means.html
dpm = {'noleap': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '365_day': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'standard': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'gregorian': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'proleptic_gregorian': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'all_leap': [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '366_day': [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '360_day': [0, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]}

def leap_year(year, calendar='standard'):
    """Determine if year is a leap year"""
    leap = False
    if ((calendar in ['standard', 'gregorian',
        'proleptic_gregorian', 'julian']) and
        (year % 4 == 0)):
        leap = True
        if ((calendar == 'proleptic_gregorian') and
            (year % 100 == 0) and
            (year % 400 != 0)):
            leap = False
        elif ((calendar in ['standard', 'gregorian']) and
                 (year % 100 == 0) and (year % 400 != 0) and
                 (year < 1583)):
            leap = False
    return leap

def get_dpm(time, calendar='standard'):
    """
    return a array of days per month corresponding to the months provided in `months`
    """
    month_length = np.zeros(len(time), dtype=np.int)

    cal_days = dpm[calendar]

    for i, (month, year) in enumerate(zip(time.month, time.year)):
        month_length[i] = cal_days[month]
        if leap_year(year, calendar=calendar) and month == 2:
            month_length[i] += 1
    return month_length


# Seasonal climatology (on monthly data set)
def season_clim(ds, calendar='standard', skipna=False):
    # Make a DataArray with the number of days in each month, size = len(time)
    month_length = xr.DataArray(get_dpm(ds.time.to_index(), calendar=calendar),
                                coords=[ds.time], name='month_length')
    # Calculate the weights by grouping by 'time.season'
    weights = month_length.groupby('time.season') / month_length.groupby('time.season').sum()

    # Test that the sum of the weights for each season is 1.0
    np.testing.assert_allclose(weights.groupby('time.season').sum().values, np.ones(4))

    # Calculate the weighted average
    with xr.set_options(keep_attrs=True):
        return (ds * weights).groupby('time.season').sum(dim='time', skipna=skipna)


# Custom seasonal climatology (on monthly data set, include just month)
def custom_season_clim(ds, calendar='standard', season=1, skipna=False):
    month_length = xr.DataArray(get_dpm(ds.time.to_index(), calendar=calendar), coords=[ds.time], name='month_length')
    
    # Deal with custom season (string or int for single month)
    month = ds['time.month']
    
    if isinstance(season, int):
        season_sel = (month == season)
    elif isinstance(season, str) and len(season) > 1:
        season_str = 'JFMAMJJASONDJFMAMJJASOND'
        
        month_start = season_str.index(season) + 1
        month_end = month_start + len(season) - 1

        if month_end > 12:
            month_end -= 12
            season_sel = (month >= month_start) | (month <= month_end)
        else:
            season_sel = (month >= month_start) & (month <= month_end)
        
    else:
        raise ValueError('The season is not valid (string or int for single month)')
        
    seasonal_data = ds.sel(time=season_sel)
    weights = month_length.sel(time=season_sel) / month_length.astype(float).sel(time=season_sel).sum()
    np.testing.assert_allclose(weights.sum().values, np.ones(1))
    
    with xr.set_options(keep_attrs=True):
        if isinstance(season, int):
            return (seasonal_data * weights).sum(dim='time', skipna=skipna).assign_coords(month=season)
        elif isinstance(season, str) and len(season) > 1:
            return (seasonal_data * weights).sum(dim='time', skipna=skipna).assign_coords(season=season)
    

# Climatology (on monthly data set)
def clim(ds, calendar='standard', skipna=False):
    month_length = xr.DataArray(get_dpm(ds.time.to_index(), calendar=calendar), coords=[ds.time], name='month_length')
    weights = month_length / month_length.sum()
    np.testing.assert_allclose(weights.sum().values, np.ones(1))
    with xr.set_options(keep_attrs=True):
        return (ds * weights).sum(dim='time', skipna=skipna)
    

# Yearly mean (on monthly data set)
def year_mean(da, calendar='standard', season='annual', skipna=False):
    # season = 'DJF' can be string
    # season = 1 or int for a single month

    month_length = xr.DataArray(get_dpm(da.time.to_index(), calendar=calendar), coords=[da.time], name='month_length')
    # Deal with custom season (string or int for single month)
    month = da['time.month']

    if isinstance(season, int):
        season_sel = (month == season)
        with xr.set_options(keep_attrs=True):
            season_mean = da.sel(time=season_sel)

    elif isinstance(season, str) and len(season) > 1:
        
        if season == 'annual':
            normalize = month_length.astype(float).groupby('time.year').sum()
            weights = month_length.groupby('time.year') / normalize
            np.testing.assert_allclose(weights.groupby('time.year').sum().values, np.ones(normalize.year.size))
            with xr.set_options(keep_attrs=True):
                season_mean = (da * weights).groupby('time.year').sum(dim='time', skipna=skipna)
        
        else:
            season_str = 'JFMAMJJASONDJFMAMJJASOND'

            month_start = season_str.index(season) + 1
            month_end = month_start + len(season) - 1

            if month_end > 12:
                # Remove one year (.isel(time=slice(month_end,-(12-month_start+1)))) to have continious months
                # The month/year label is from the starting month

                # Checked with cdo: !cdo yearmonmean -selmon,10,11,12 -shifttime,-2mo in.nc out.nc
                # -> slight differences, is CDO do not take the right month weights when shifted?
                # -> or do I use the wrong weights?
                # https://code.mpimet.mpg.de/boards/1/topics/826
                # 
                # !cdo yearmean -selmon,10,11,12 -shifttime,-2mo in.nc out.nc
                # Same results with the calendar=360_day
                #
                # Try with cdo season selection?
                
                # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

                month_end -= 12
                season_sel = (month >= month_start) | (month <= month_end)
                seasonal_data = da.sel(time=season_sel).isel(time=slice(month_end,-(12-month_start+1)))
                seasonal_month_length = month_length.astype(float).sel(time=season_sel).isel(time=slice(month_end,-(12-month_start+1)))
                weights = xr.DataArray(
                   [value/seasonal_month_length.resample(time='AS-'+cld.month_abbr[month_start]).sum().values[i//len(season)] \
                         for i, value in enumerate(seasonal_month_length.values)],
                    coords = [month_length.sel(time=season_sel).isel(time=slice(month_end,-(12-month_start+1))).time],
                    name = 'weights'
                                      )
                sum_weights = weights.resample(time='AS-'+cld.month_abbr[month_start]).sum()
                np.testing.assert_allclose(sum_weights.values, np.ones(sum_weights.size))
                with xr.set_options(keep_attrs=True):
                    season_mean = (seasonal_data * weights).resample(time='AS-'+cld.month_abbr[month_start])\
                                                           .sum('time', skipna=skipna)
                # To keep same format as the version bellow (be aware that the year label will be from the first month)
                season_mean = season_mean.assign_coords({"time": season_mean['time.year']})
                season_mean = season_mean.rename({'time': 'year'})


            else:
                # Checked with CDO (!cdo yearmonmean -selmonth,'' in.nc out.nc)
                season_sel = (month >= month_start) & (month <= month_end)
                seasonal_data = da.sel(time=season_sel)
                normalize = month_length.astype(float).sel(time=season_sel).groupby('time.year').sum()
                weights = month_length.sel(time=season_sel).groupby('time.year') / normalize
                np.testing.assert_allclose(weights.groupby('time.year').sum().values, np.ones(normalize.size))
                with xr.set_options(keep_attrs=True):
                    season_mean = (seasonal_data * weights).groupby('time.year').sum('time', skipna=skipna)


    else:
        raise ValueError('The season is not valid (string or int for single month)')
        
    return season_mean

# Annual cycle (on monthly data set)
def annual_cycle(ds, calendar='standard', skipna=False):
    month_length = xr.DataArray(get_dpm(ds.time.to_index(), calendar=calendar), coords=[ds.time], name='month_length')
    weights = month_length.groupby('time.month') / month_length.astype(float).groupby('time.month').sum()
    np.testing.assert_allclose(weights.groupby('time.month').sum().values, np.ones(12))
    with xr.set_options(keep_attrs=True):
        return (ds * weights).groupby('time.month').sum(dim='time', skipna=skipna)



# =============================================================================
# Compute spatial average
# =============================================================================
# https://pangeo.io/use_cases/physical-oceanography/sea-surface-height.html
def spatial_average(da):
    
    # Get the longitude and latitude names + other dimensions to test that the sum of weights is right
    lat_str = ''
    lon_str = ''
    other_dims_str = []
    for dim in da.dims:
        if dim in ['lat', 'latitude']: 
            lat_str = dim
        elif dim in ['lon', 'longitude']: 
            lon_str = dim
        else:
            other_dims_str.append(dim)
    
    # Compute the weights
    coslat = np.cos(np.deg2rad(da.lat)).where(~da.isnull())
    weights = coslat / coslat.sum(dim=(lat_str, lon_str))
    
    # Test that the sum of weights equal 1
    np.testing.assert_allclose(
        weights.sum(dim=(lat_str,lon_str)).values, 
        np.ones([da.coords[dim_str].size for dim_str in other_dims_str]),
        rtol=1e-06
    )
    
    with xr.set_options(keep_attrs=True):
        return (da * weights).sum(dim=(lat_str,lon_str))
    

    
# =============================================================================
# Add cyclic point
# =============================================================================
# https://github.com/darothen/plot-all-in-ncfile/blob/master/plot_util.py
def cyclic_dataarray(da, coord='lon'):
    """ Add a cyclic coordinate point to a DataArray along a specified
    named coordinate dimension.
    """
    assert isinstance(da, xr.DataArray)

    lon_idx = da.dims.index(coord)
    cyclic_data, cyclic_coord = add_cyclic_point(da.values,
                                                 coord=da.coords[coord],
                                                 axis=lon_idx)

    # Copy and add the cyclic coordinate and data
    new_coords = dict(da.coords)
    new_coords[coord] = cyclic_coord
    new_values = cyclic_data

    new_da = xr.DataArray(new_values, dims=da.dims, coords=new_coords)

    # Copy the attributes for the re-constructed data and coords
    for att, val in da.attrs.items():
        new_da.attrs[att] = val
    for c in da.coords:
        for att in da.coords[c].attrs:
            new_da.coords[c].attrs[att] = da.coords[c].attrs[att]

    return new_da


# =============================================================================
# Zones
# =============================================================================
# HK: Hindu-Kush / Karakoram / Western Himalay
# HM: Central and Est Himalaya
# TB: Tibetan Plateau
def get_zones_IPSL_CM6A_LR():
    # Grid size for LMDZ
    dx=2.5
    dy=1.2676

    lonlim_HK=(70-dx/2, 70-dx/2 + 10+dx)
    latlim_HK=(31.690142-dy/2, 31.690142-dy/2 + 7.6056339+dy)
    
    lonlim_HM=(77.5-dx/2+dx, 77.5-dx/2+dx + 15+2*dx)
    latlim_HM=(26.619719-dy/2, 26.619719-dy/2 + 3.802816+dy)

    lonlim_TB=(82.5-dx/2, 82.5-dx/2 + 15+3*dx)
    latlim_TB=(31.690142-dy/2, 31.690142-dy/2 + 7.6056339)
    
    return lonlim_HK, latlim_HK, lonlim_HM, latlim_HM, lonlim_TB, latlim_TB

import matplotlib.patches as mpatches
import cartopy.crs as ccrs

def plot_zones_IPSL_CM6A_LR(ax):
    # Grid size for LMDZ
    dx=2.5
    dy=1.2676
    
    ax.text(70-dx/3, 31.690142-dy/2+7.6056339-3*dy/4, 'HK')
    ax.add_patch(mpatches.Rectangle(
            xy=[70-dx/2, 31.690142-dy/2], width=10+dx, height=7.6056339+1*dy,
            transform=ccrs.PlateCarree(), fill=False
        ))
    ax.text(77.5+dx-dx/3, 26.619719-dy/2+3.802816-3*dy/4, 'HM')
    ax.add_patch(mpatches.Rectangle(
            xy=[77.5-dx/2+dx, 26.619719-dy/2], width=15+2*dx, height=3.802816+dy,
            transform=ccrs.PlateCarree(), fill=False
        )) # CH
    ax.text(82.5-dx/3, 31.690142-dy/2+7.6056339-dy-3*dy/4, 'TB')
    ax.add_patch(mpatches.Rectangle(
            xy=[82.5-dx/2, 31.690142-dy/2], width=15+3*dx, height=7.6056339,
            transform=ccrs.PlateCarree(), fill=False
        )) # TP
    
    return None
