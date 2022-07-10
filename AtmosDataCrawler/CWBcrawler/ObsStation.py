
from AtmosDataCrawler.core._data_writter import _writter
from pandas import date_range, concat, read_html, DataFrame
from time import sleep
from pathlib import Path

# https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp
class setting(_writter):

	nam = 'CWB_ObsStation'

	def _crawl(self,_tm):
		_index = date_range(_tm,periods=24,freq='1h')

		try:
			print(f'crawl date : {_tm}')
			_df = read_html(self.url_ori.format(_tm),skiprows=2,header=0,na_values=['...','V'])[0].set_index(_index)

			sleep(.4)

			return _df

		except ImportError:
			raise ImportError('Pls install BeautifulSoup4 and html5lib')

		except Exception as err:
			print(f'{_tm} fail : {err}')
			return DataFrame(index=_index)

	def crawl(self,stnam):

		## process with old version python
		if self._old_ver:
			_jsn2df = self.info
			self.info = DataFrame(_jsn2df['data'],index=_jsn2df['index'],columns=_jsn2df['columns'],)

		## get meta information and set class parameter
		try:
			_st_no, _st_alt, _ = self.info.loc[stnam].values
		except KeyError as k:
			_err_msg = []
			for _count, _df in self.info.groupby('county'):
				_err_msg.append(f'{_count} :\n'+' '.join(_df.index.to_list())+'\n\n')
			_err_msg = '\n'+''.join(_err_msg)+f'{k} not in the CWB station'

			raise ValueError(_err_msg)

		self.url_ori = f'http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station={_st_no}&stname=&datepicker={{}}&altitude={_st_alt}m'
		_dl_index = self.dl_index.strftime('%Y-%m-%d')

		## run
		if self.parallel:
			from multiprocessing import Pool, cpu_count

			pool = Pool(cpu_count())
			_df_lst = pool.map(self._crawl,_dl_index)
			pool.close()
			pool.join()

		else:
			_df_lst = []
			for _tm in _dl_index:
				_df = self._crawl(_tm)

				_df_lst.append(_df)

		## output
		_df_out = concat(_df_lst).reindex(self.tm_index).apply(to_numeric,errors='coerce')
		_df_out.index.name = 'Time'

		## save data
		print()
		self.out_info = stnam
		self._save_out(_df_out)

		return _df_out




class __update:

	nam = 'CWB_ObsStation'

	## update information data
	def __init__(self):
		from pandas import read_csv
		import pickle as pkl
		import json as jsn

		## parameter 
		_update_info_path = Path('AtmosDataCrawler')/'core'/'utils'/self.nam

		## read csv file, then return dataframe
		with (_update_info_path/'info.csv').open('r',encoding='utf-8',errors='ignore') as f:
			_info = read_csv(f).set_index('stNam')[['stNo','altitude','county']]

		## output pickle
		with (_update_info_path/'info.pkl').open('wb') as f:
			pkl.dump(_info,f,protocol=pkl.HIGHEST_PROTOCOL)

		## python version < 3.8, can not read the .pkl file of protocol 5
		with (_update_info_path/'info.json').open('w',encoding='utf-8',errors='ignore') as f:

			_info = jsn.loads(_info.to_json(orient='split'))
			jsn.dump(_info,f)