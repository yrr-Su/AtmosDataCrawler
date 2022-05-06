
from AtmosDataCrawler.core._data_writter import _writter
from pandas import date_range, concat, DataFrame
import requests
# from time import sleep
from pathlib import Path

# https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp
class setting(_writter):

	nam = 'EPA_ObsStation'

	def _crawl(self,_tm):


	def crawl(self,stnam):
		



	## update information data
	def _setting__update_info(self):

		print('it works ~')
		## read json file, then return dict
		pass