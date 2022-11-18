from logging.config import dictConfig
import logging
from colorlog import ColoredFormatter
import threading
from queue_item import SiteEntry
from monitor import Monitor, MonitoringQueue
import rest


def main():
  """
  The main function. Listenes to the queue and fires of monitoring threads as needed
  """

  configure_logging()

  req_queue = MonitoringQueue.get_queue()
  launch_api()

  logging.debug("In main function")
  logging.debug(f"Queue size current: {req_queue.qsize()}")

  while True:
    if not req_queue.empty():
      monitor = req_queue.get()
      logging.debug(f"site_entry.active: {monitor.active}")
      if monitor.active:
        logging.debug(f"Starting run for {monitor.name}")
        start_run(monitor)
        req_queue.task_done()
      elif not monitor.active:
        stop_run(monitor)
      else:
        raise ValueError(f"Invalid value for <entity>.active, must be true or false, got {monitor.active}")


def launch_api():
  """
  Function responsible for launching the API server
  """
  logging.info(f"Starting API server")
  rest.start_server()


def start_run(item: SiteEntry):
  """
  Initialise a run for a site
  """
  monitor = Monitor(item)
  logging.info(monitor)
  logging.info(f"Starting thread on {monitor.name}")
  threading.Thread(target=monitor.start_monitor, args=[]).start()


def stop_run(monitor: Monitor):
  """
  Stop a run for a site
  """
  monitor.stop_monitor()


def configure_logging() -> None:
  """
  Setup logging
  """
  log_level = logging.INFO
  logging.root.setLevel(log_level)
  log_format = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
  formatter = ColoredFormatter(log_format)

if __name__ == "__main__":
  main()