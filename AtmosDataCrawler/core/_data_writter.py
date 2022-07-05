
from pathlib import Path
from pandas import date_range
from datetime import datetime as dtm
from datetime import timedelta as dtmdt
import pickle as pkl
import json as jsn


# parents class for write out the data
# support csv, excel, pickle
class _writter:
	
	nam = None
	out_info = 'crawl'

	def __init__(self,path=None,start=None,end=None,parallel=False,
				 csv=True,excel=False,pickle=False,
				 __old_ver_test=False):

		## default parameter
		path  = path  or Path('.')
		start = start or (dtm.now()-dtmdt(days=2))
		end	  = end   or (dtm.now()-dtmdt(days=1))

		## class parameter
		self._old_ver = False
		self.parallel = parallel
		self.dl_index = date_range(start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'),freq='1d')
		self.tm_index = date_range(self.dl_index[0],self.dl_index[-1]+dtmdt(days=1),freq='1h')[:-1]

		## output parameter
		self.path	= Path(path)
		self.csv	= csv
		self.excel	= excel
		self.pickle	= pickle

		## meta information
		try:
			with (Path(__file__).parent/'utils'/self.nam/'info.pkl').open('rb') as f:
				self.info = pkl.load(f)
				if __old_ver_test: raise ValueError
		except ValueError:
			with (Path(__file__).parent/'utils'/self.nam/'info.json').open('r') as f:
				self.info = jsn.load(f)
				self._old_ver = True

	## write out data
	def _save_out(self,_df_out):

		_st, _ed = self.dl_index.strftime('%Y%m%d')[[0,-1]]
		_out_nam = f"{self.out_info}_{self.nam}_{_st}_{_ed}"
		self.path.mkdir(exist_ok=True,parents=True)
	
		if self.csv:
			print(f'save : {_out_nam}.csv\n')
			_df_out.to_csv(self.path/f'{_out_nam}.csv')

		if self.excel:
			print(f'save : {_out_nam}.xlsx\n')
			from pandas import ExcelWriter
			with ExcelWriter(self.path/f'{_out_nam}.xlsx') as f:
				_df_out.to_excel(f,sheet_name=self.nam)

		if self.pickle:
			print(f'save : {_out_nam}.pkl\n')
			with (self.path/f'{_out_nam}.pkl').open('wb') as f:
				pkl.dump(_df_out,f,protocol=pkl.HIGHEST_PROTOCOL)

	## update information file in utils
	def __update_info(self,):
		pass