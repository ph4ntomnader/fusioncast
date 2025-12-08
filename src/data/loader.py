import os
from datetime import datetime, timedelta
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

class NEXRADLoader:
    def __init__(self, cache_dir: Optional[Path] = '/data/cache/', data_dir: Optional[Path] = '/data/raw/'):
        if not NEXRAD_AVAILABLE:
            raise ImportError("NexradAwsInterface is not available. Please check NexradAWS installation.")
        self.nexrad = NexradAwsInterface()
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download_scans(self, station: 'KTLX', start_time: datetime, end_time: datetime) -> List[Path]:     # set station from which to download data in station: str argument
        scans = self.nexrad.get_scans_in_range(station, start_time, end_time)
        downloaded_files = []
        for scan in scans:
            local_path = self.cache_dir / scan.object_key
            if not local_path.exists():
                self.nexrad.download_scan(scan, str(local_path))
            downloaded_files.append(local_path)
        return downloaded_files