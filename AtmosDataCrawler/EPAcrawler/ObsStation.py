
from AtmosDataCrawler.core._data_writter import _writter
from pandas import date_range, concat, DataFrame
import requests
# from time import sleep
from pathlib import Path

# https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp
class setting(_writter):

	nam = 'EPA_ObsStation'

	def _crawl(self,_tm):
		pass

	def crawl(self,stnam):
		pass



	## update information data
	def _setting__update_info(self):
		from pandas import read_csv
		import pickle as pkl
		import json as jsn
		import numpy as n

		## read json and csv, then return dict

		## station nam and county id
		## 1. api has expiration date
		## 2. station information may be change
		##	  download the information : 
		##	  https://data.epa.gov.tw/dataset -> 資料目錄 -> 資料集清單下載 CSV -> 環保署開放資料清單.csv
		with (self._update_info_path/'環保署開放資料清單.csv').open('r',encoding='utf-8',errors='ignore') as f:
			_df	 	= read_csv(f)[['資料集名稱','資料集代碼']]
			_df_air = _df.loc[_df['資料集代碼'].str.find('AQX')==0].copy()

			_df_sta    = _df_air.loc[_df_air['資料集名稱'].str.find('空氣品質小時值')==0].copy()
			_df_county = _df_air.loc[_df_air['資料集名稱'].str.find('縣市(')==0].copy()

			_, _county, _station = n.array(_df_sta['資料集名稱'].apply(lambda _: _[:-1].split('_')).copy().to_list()).T

			_df_nam = DataFrame({'county':_county}).set_index(_station)
			_df_id  = _df_county.set_index(_df_county['資料集名稱'].apply(lambda _: _[3:-8]).copy())['資料集代碼']
			
			_df_out = []
			for _grp, _df in _df_nam.groupby('county'):
				_df['id'] = _df_id[_df.values[0,0]]
				_df_out.append(_df)
			
			_df_out = concat(_df_out)


		## api and expiration date
		with (self._update_info_path/'info.json').open('r',encoding='utf-8',errors='ignore') as f:
			_info = jsn.load(f)

		_info['df_id'] = _df_out

		with (self._update_info_path/'info.pkl').open('wb') as f:
			pkl.dump(_info,f,protocol=pkl.HIGHEST_PROTOCOL)


