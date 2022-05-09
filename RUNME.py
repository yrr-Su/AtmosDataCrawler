




import sys
from pathlib import Path
from datetime import datetime as dtm
from datetime import timedelta as dtmdt


# AtmosDataCrawler
## parameter
PATH_OUT = Path('RUNME')
PATH_OUT.mkdir(exist_ok=True)

## use CWB crawler
## crawl observation data
from AtmosDataCrawler.CWBcrawler import ObsStation
cwb_obs = ObsStation.setting(path=PATH_OUT,start=dtm.now()-dtmdt(days=8),end=dtm.now()-dtmdt(days=1),parallel=True,
							 pickle=False,csv=True,excel=False)

## use EPA crawler
## crawl observation data
from AtmosDataCrawler.EPAcrawler import ObsStation
epa_obs = ObsStation.setting(path=PATH_OUT,start=dtm.now()-dtmdt(days=2),end=dtm.now()-dtmdt(days=1),parallel=False,
							 pickle=False,csv=False,excel=True)



if __name__=='__main__':

	print('\nThis is sample code of this model : AtmosDataCrawler')
	print('This code will download the CWB station("臺北") and EPA station("古亭")\n\n')

	df_TP = cwb_obs.crawl('臺北')
	df_GT = epa_obs.crawl('古亭')



