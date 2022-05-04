# CWBcrawler

Crawl the data from Central Weather Bureau 

## User Guide

### required package

* pandas
* BeautifulSoup4
* html5lib

### setting parameter

CWBcrawler.<module>.setting(path=None, start=None, end=None, parallel=False,
csv=True, excel=False, pickle=False)

- **path** : *str or pathlib-like, default is current path('.')*
	- Path of output file
- **start**: *str or datetime-like, default is the day before yesterday*
	- Left bound for download data
- **end**: *str or datetime-like, default is yesterday*
	- Right bound for download data
- **parallel**: *bool, default False*
	- Multipleprocessing for download long period data
	- The main code should run under  `if __name__ == '__main__':`
- **csv**: *bool, default False*
	- Output *.csv* file
- **excel**: *bool, default False*
	- Output *.xlsx* file
- **pickle**: *bool, default False*
	- Output *.pkl* file

### sample code

```python
import sys
from pathlib import Path
sys.path.insert(1,Path('C:/')/'Users'/'your_name'/'Desktop'/'CWBcrawler')

from datetime import datetime as dtm
from datetime import timedelta as dtmdt

from CWBcrawler import ObsDtCrawler


obs = ObsDtCrawler.setting(path=Path(),start=dtm(2022,4,11),end=dtm(2022,4,13),
                           parallel=False,
						   pickle=True,csv=True,excel=True)


if __name__=='__main__':
	df = obs.crawl('臺中')





```



### obsDtCrawler

Observation data from CWB stations

https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp

---

obsDtCrawler.setting.crawl(stnam)

- **stnam** : *str*
	- Station name in Chinese



