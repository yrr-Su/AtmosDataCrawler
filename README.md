# AtmosDataCrawler

Author : yrr-Su 

## User Guide

### required package

* pandas
* BeautifulSoup4
* html5lib

## structure

* AtmosDataCrawler
  * EPAcrawler
    * ObsStation
  * CWBcrawler
    * ObsStation
    * WeatherGraphs (coming soon...)

## sample code

```python
import sys
from pathlib import Path
from datetime import datetime as dtm

# AtmosDataCrawler
## add file path of folder into python namespace
sys.path.insert(1,str(Path('C:/')/'Users'/'name'/'Desktop'/'AtmosDataCrawler'))

## use CWB crawler
## crawl observation data
from AtmosDataCrawler.CWBcrawler import ObsStation
cwb_obs = ObsStation.setting(start=dtm(2022,4,11),end=dtm(2022,4,12),parallel=False,
						 pickle=False,csv=True,excel=False)

## use EPA crawler
## crawl observation data
from AtmosDataCrawler.EPAcrawler import ObsStation
epa_obs = ObsStation.setting(start=dtm(2022,4,11),end=dtm(2022,4,12),parallel=True,
						 pickle=False,csv=False,excel=True)




if __name__=='__main__':
	df_XT = cwb_obs.crawl('西屯')
	df_CM = epa_obs.crawl('忠明')




```



## config setting parameter

AtmosDataCrawler.< source module >.< data getter module >.setting(path=None, start=None, end=None, parallel=False,
csv=True, excel=False, pickle=False)

- **path** : *str or pathlib-like, default is current path('.')*
  - Path of output file
- **start**: *str or datetime-like, default is the day before yesterday*
  - Left bound for download data
- **end**: *str or datetime-like, default is yesterday*
  - Right bound for download data, set the value same with **start** if collect one-day-data
- **parallel**: *bool, default False*
  - Multipleprocessing for download long period data
  - The main code should run under  `if __name__ == '__main__':`
- **csv**: *bool, default False*
  - Output *.csv* file
- **excel**: *bool, default False*
  - Output *.xlsx* file
- **pickle**: *bool, default False*
  - Output *.pkl* file

## source model

### CWBcrawler

---

#### ObsStation

Observation data from CWB stations

https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp

ObsStation.setting.crawl(stnam)

- **stnam** : *str*
  - Station name in Chinese

### EPAcrawler

---

#### ObsStation

Observation data from EPA stations API

Have to update API once a year

[首頁 | 環保署環境資料開放平臺 (epa.gov.tw)](https://data.epa.gov.tw/)

ObsStation.setting.crawl(stnam)

- **stnam** : *str*
  - Station name in Chinese
