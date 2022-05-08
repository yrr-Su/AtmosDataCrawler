
from AtmosDataCrawler.core._data_writter import _writter
from pandas import date_range, concat, DataFrame, to_datetime
import requests
import json as jsn
from datetime import datetime as dtm
from pathlib import Path
import numpy as n

# https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp
class setting(_writter):

	nam = 'EPA_ObsStation'

	def _crawl(self,_off):
		try:
			print(f'crawl offset : {_off}')
			_resp = requests.get(self.url_ori.format(_off))

			if _resp.status_code>400:
				_resp.raise_for_status()

		except requests.exceptions.SSLError:
			ImportError('SSL model not found, please activate conda enviroment (https://conda.io/activation)')

		## parse the crawled text
		_resp_dt = jsn.loads(_resp.text)['records']

		if len(_resp_dt)==0:
			return None
		else:
			return DataFrame(_resp_dt)


	def crawl(self,stnam):
		## get meta information and set class parameter
		try:
			_api   = self.info['api']
			_st_id = self.info['df_id'].loc[stnam].values[-1]
			
			## check out the api time
			if dtm.now()>=dtm.strptime(self.info['api_end'],'%Y-%m-%d %X'):
				raise ValueError('Update EPA api code')

		except KeyError as k:
			err_msg = 'error message'

			raise ValueError(err_msg)

		_dl_index = self.tm_index[[0,-1]].strftime('%Y-%m-%d %H:00')
		self.url_ori = f'https://data.epa.gov.tw/api/v2/{_st_id}?format=json&offset={{}}&api_key={_api}'
		self.url_ori += f'&filters=sitename,EQ,{stnam}|monitordate,GR,{_dl_index[0]}|monitordate,LE,{_dl_index[-1]}'

		## run
		## offset 1000
		if self.parallel:
			from multiprocessing import Pool, cpu_count

			cpu_num = cpu_count()
			pool = Pool(cpu_num)

			_off_ary = n.arange(0,cpu_num*1000,1000)

			stop, _df_lst = True, []
			while stop:
				_crawl_lst = pool.map(self._crawl,_off_ary)

				for _df in _crawl_lst:
					if _df is None: 
						stop = False

				_df_lst.append(concat(_crawl_lst))

				_off_ary += cpu_num*1000

			pool.close()
			pool.join()

		else:
			_df_lst, _off, _df = [], 0, True
			
			while _df is not None:
				_df = self._crawl(_off)
				_df_lst.append(_df)
				
				_off += 1000

		## data pre-process
		_df_out = concat(_df_lst)[['monitordate','itemengname','concentration']]
		_df_out = _df_out.loc[~_df_out.duplicated(subset=['monitordate','itemengname']).copy()].replace('x',n.nan)
		_df_out['monitordate'] = to_datetime(_df_out['monitordate'].copy())
		
		_df_out = _df_out.pivot_table(index='monitordate',columns='itemengname',values='concentration',
									  aggfunc=n.sum).astype(float).reindex(self.tm_index)

		## save data
		print()
		self._save_out(_df_out)

		return _df_out


	## update information data
	def _setting__update_info(self):
		from pandas import read_csv
		import pickle as pkl
		import json as jsn

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


