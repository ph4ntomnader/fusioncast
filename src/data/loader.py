import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Tuple
import warnings

# ^ base library imports

try:                        # importing nexrad interface; make sure loader script is ran after .venv activation. vs code's run button may not do this.
    import boto3
    from nexradaws import NexradAwsInterface
    NEXRAD_AVAILABLE = True
except ImportError as err:
    NEXRAD_AVAILABLE = False
    warnings.warn("NexradAwsInterface could not be imported. Please check NexradAWS installation.")
    


class NEXRADLoader:                 # actual loader class for NEXRAD data
    def __init__(self, cache_dir: Optional[Path] = 'data/cache/', data_dir: Optional[Path] = 'data/raw/'):
        if not NEXRAD_AVAILABLE:
            raise ImportError("NexradAwsInterface is not available. Please check NexradAWS installation.")
        
        self.nexrad = NexradAwsInterface()
        self.cache_dir = Path(cache_dir)
        self.data_dir = Path(data_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def download_scans(self, start_time: datetime, end_time: datetime, station: str = 'KTLX') -> List[Path]:     # set station from which to download data in station: str argument
        scans = self.nexrad.get_avail_scans_in_range(start_time, end_time, station)
        scan_results = self.nexrad.download(scans, basepath=self.data_dir)
        downloaded_files = []
        for scan in scan_results.success:
                downloaded_files.append(Path(scan.filepath))
            
        return downloaded_files
    
# loader = NEXRADLoader()                         # testing the loader with small sample data
# end_time = datetime.now(timezone.utc)
# start_time = end_time - timedelta(hours=1)
# downloaded_files = loader.download_scans(start_time=start_time, end_time=end_time,station='KTLX')
# print(f"Downloaded files: {downloaded_files}")
# for file in downloaded_files:
#    print(file)