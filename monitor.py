import requests
import time
import logging
from queue_item import SiteEntry
import queue
import asyncio

logger = logging.getLogger()

class Monitor:
  """
  Class representing a Monitor.
  """

  site_entry: SiteEntry

  def __init__(self, site_entry: SiteEntry):
    self.site_entry = site_entry

  def __getattr__(self, __name: str):
    if hasattr(self.site_entry, __name):
      return getattr(self.site_entry, __name)
    return super(Monitor).__getattr__(__name)

  @staticmethod
  def _format_url(host: str, path: str = "", https: bool = True, **kwargs):
    return(f"{'https' if https else 'http'}://{host}{path}")


  async def start_monitor(self) -> any:
    logger.info("IN START_MONITOR")
    success, failure = 0, 0
    url = Monitor._format_url(host=self.site_entry.address, https=self.site_entry.https)
    logger.info(f"Starting run for {self.site_entry.name}")
    while self.site_entry.active == True:
      logger.info(f"Firing off request to {self.site_entry.name}")
      r = requests.get(url)
      if r.status_code >= 200 and r.status_code < 300:
        success += 1
      else:
        failure += 1

      logger.info(f"Request fired, sleeping for {self.site_entry.interval}. Successes so far: {success}")
      await asyncio.sleep(float(self.site_entry.interval))
  
  def stop_monitor(self):
    raise InterruptedError(f"Terminating run for {self.site_entry.name}")


class MonitoringQueue():

  _queue = None

  @staticmethod
  def get_queue():
    if MonitoringQueue._queue is None:
      MonitoringQueue._queue = asyncio.Queue()
    return MonitoringQueue._queue
