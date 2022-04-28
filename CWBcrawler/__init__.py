
from pathlib import Path
from pandas import date_range
from datetime import datetime as dtm
from datetime import timedelta as dtmdt
import pickle as pkl

# parents class for write out the data
# support csv, excel, 
class _writter:
	
	nam = None

	def __init__(self,path=None,start=None,end=None,parallel=False,
				 csv=True,excel=False,pickle=False):

		## default parameter
		path  = path  or Path('.')
		start = start or (dtm.now()-dtmdt(days=2)).strftime('%Y-%m-%d')
		end	  = end   or (dtm.now()-dtmdt(days=1)).strftime('%Y-%m-%d')

		## class parameter
		self.parallel = parallel
		self.dl_index = date_range(start,end,freq='1d')
		self.tm_index = date_range(self.dl_index[0],self.dl_index[-1]+dtmdt(days=1),
								   closed='left',freq='1h')

		## output parameter
		self.path	= path
		self.csv	= csv
		self.excel	= excel
		self.pickle	= pickle

		## get meta information
		with (Path('utils')/f'{self.nam}.pkl').open('rb') as f:
			self.info = pkl.load(f)

