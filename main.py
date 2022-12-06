from logging.config import dictConfig
import logging
from colorlog import ColoredFormatter
from queue_item import SiteEntry
from monitor import Monitor, MonitoringQueue
import rest
import asyncio
from asyncio import Task
from typing import List

async def main():
  """
  The main function. Listenes to the queue and fires of monitoring threads as needed
  """

  configure_logging()

  req_queue = MonitoringQueue.get_queue()
  await launch_api()
  while True:
    if not req_queue.empty():
      logging.info(f" Queue size: {req_queue.qsize()}")
      monitor = await req_queue.get()
      if monitor.active:
        logging.info(f"Active for {monitor.name} set, creating task.")
        #run = create_task(start_run(monitor))
        #logging.info(f"Async task created for {run.get_name()}")
        logging.info(f"Awaiting start_run")
        #await run
        await start_run(monitor)
        logging.info(f"Task started, marking as done in queue.")
        req_queue.task_done()
      elif not monitor.active:
        logging.info(f"Active for {monitor.name} is false, cancelling run.")
        #run.cancel()
        stop_run(monitor)
      else:
        raise ValueError(f"Invalid value for <entity>.active, must be true or false, got {monitor.active}")


async def launch_api():
  """
  Function responsible for launching the API server
  """
  logging.info(f"Starting API server")
  await rest.start_server()


async def start_run(monitor: Monitor):
  """
  Initialise a run for a site
  """
  logging.info(f"Starting thread on {monitor.name}")
  while True:
    res = await monitor.start_monitor()
    if res.status_code >= 200 and res.status_code < 300:
      success += 1
    else:
      failure += 1
    logging.info(f"Request sent, now sleeping")
    asyncio.sleep(monitor.site_entry.interval)
    logging.info(f"sleep done")


def stop_run(monitor: Monitor):
  """
  Stop a run for a site
  """
  monitor.stop_monitor()


async def create_task(item: SiteEntry) -> Task:
  logging.info(f"Name is {item.name}")
  task = asyncio.create_task(
    start_run(item),
    name=item.name
  )
  logging.info=(f"Created task: {task}")
  return task


def configure_logging() -> None:
  """
  Setup logging
  """
  log_level = logging.DEBUG
  log_format = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
  formatter = ColoredFormatter(log_format)

  stream = logging.StreamHandler()
  stream.setLevel(log_level)
  stream.setFormatter(formatter)

  logging.root.setLevel(log_level)
  logging.root.addHandler(stream)

if __name__ == "__main__":
  asyncio.run(main())