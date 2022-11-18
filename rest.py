import json
from flask import Flask, jsonify, request
from queue_item import SiteEntry
from main import MonitoringQueue, Monitor


def start_server():
  app = Flask(__name__)

  @app.route('/')
  def index():
    return(jsonify({"status": "healthy"}), 200)

  @app.route('/add-item', methods=["POST", "PUT"])
  def add_item():
    raw = request.json
    queue_item = Monitor(SiteEntry(**raw))
    queue = MonitoringQueue.get_queue()
    try:
      queue.put(queue_item)
      return("", 201)
    except:
      raise ValueError(f"Unable to add {queue_item} to queue")

  app.run(debug=True)