from flask import Flask, jsonify, request
from flask.logging import default_handler
from queue_item import SiteEntry
from main import MonitoringQueue, Monitor
import asyncio
import logging


async def start_server():
  app = Flask(__name__)
  logger = logging.getLogger()
  logger.addHandler(default_handler)

  @app.route('/')
  def index():
    return(jsonify({"status": "healthy"}), 200)

  @app.route('/add-item', methods=["POST", "PUT"])
  async def add_item():
    raw = request.json
    queue_item = Monitor(SiteEntry(**raw))
    queue = MonitoringQueue.get_queue()
    try:
      await queue.put(queue_item)
      return("", 201)
    except:
      raise ValueError(f"Unable to add {queue_item.name} to queue")

  app.run(debug=True)