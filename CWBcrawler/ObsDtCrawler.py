
from . import _writter
from pandas import date_range, concat, read_html, DataFrame
from time import sleep
from pathlib import Path

# https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp
class setting(_writter):

	nam = 'obsDt'

	def _crawl(self,_tm):
		_index = date_range(_tm,periods=24,freq='1h')

		try:
			_df = read_html(self.url_ori.format(_tm),skiprows=2,header=0,na_values=['...'])[0].set_index(_index)

			print(f'{_tm}')
			sleep(.4)

			return _df

		except ImportError:
			raise ImportError('Pls install BeautifulSoup4 and html5lib')

		except Exception as err:
			print(f'{_tm} fail : {err}')
			return DataFrame(index=_index)

	def crawl(self,stnam):
		
		## get meta information and set class parameter 
		_st_no, _st_alt = self.info.loc[stnam].values
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
		_df_out = concat(_df_lst).reindex(self.tm_index)

		## save data
		print()
		self._save_out(_df_out)

		return _df_out