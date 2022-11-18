import logging

class SiteEntry:

  def __init__(self, name: str, address: str, https: bool, interval: float, active: bool) -> None:
    self.name = name
    self.address = address
    self.https = https
    self.interval = interval
    self._active: bool = active

  @property
  def active(self) -> bool:
    logging.debug(f"Getter for _active called")
    return self._active

  @active.setter
  def active(self, active):
    if active:
      self._active = active
    else:
      raise ValueError(f"Invalid value for active, got {active.lower()}, need to be true or false")

    
