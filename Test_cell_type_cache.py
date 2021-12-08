#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 09:47:28 2021

@author: julienballbe
"""
#%% import needed packages
from allensdk.core.cell_types_cache import CellTypesCache
import pandas
from allensdk.api.queries.cell_types_api import CellTypesApi
#%%The manifest_file argument
# tells it where to store the manifest, which is a JSON file that tracks
# file paths. 
ctc= CellTypesCache(manifest_file="my_testfile/manifest_bis.json")

#%% Dowload the cells you want --> here mouse
mycells=ctc.get_cells(require_morphology=False,
                      require_reconstruction=False,
                      species=[CellTypesApi.MOUSE])



#%%
print(mycells[1].keys())
if 'reporter_jhbstatus' in mycells[1].keys():
    print('okokok')
#%% Create sub dataframes
area_dict={}
for elt in range(0,len(mycells)):
    current_area=mycells[elt].get("structure_area_abbrev")
    print(elt)
    if current_area in area_dict.keys():
        area_dict[current_area]+=1
    else:
        area_dict[current_area]=1
        
print('ok')
        
    
#%%

data_set=ctc.get_ephys_data(mycells[0]['id'])

#%%
mysweeps=data_set.get_sweep_numbers()
#%%
my_spikes=data_set.get_spike_times(100)
#%%
ephys_features=ctc.get_ephys_features(dataframe=True)
#%%
colnames=list(ephys_features.columns)

#%%
my_specimen=565236919
my_spe_data_set=ctc.get_ephys_data(my_specimen)
my_spe_sweep_nb=my_spe_data_set.get_sweep_numbers()
my_spe_spike_times=my_spe_data_set.get_spike_times(33)
my_spe_ephys_features=ctc.get_ephys_features(565236919)

#%%
from allensdk.core.nwb_data_set import NwbDataSet
my_sweep=my_spe_data_set.get_sweep(101)

#%%
import matplotlib.pyplot as plt
import numpy as np
index_range = my_sweep["index_range"]
i=my_sweep["stimulus"][0:index_range[1]+1]
v=my_sweep["response"][0:index_range[1]+1]
i*=1e12
v*=1e3

sampling_rate = my_sweep["sampling_rate"] # in Hz
t = np.arange(0, len(v)) * (1.0 / sampling_rate)

plt.style.use('ggplot')
fig, axes = plt.subplots(2, 1, sharex=True)
axes[0].plot(t, v, color='black')
axes[1].plot(t, i, color='gray')
axes[0].set_ylabel("mV")
axes[1].set_ylabel("pA")
axes[1].set_xlabel("seconds")
plt.xlim([1.9,2.3])
plt.show()
