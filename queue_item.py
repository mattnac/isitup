import logging


class SiteEntry:

  def __init__(self, name: str, address: str, https: bool, interval: float, active: bool) -> None:
    self.name = name
    self.address = address
    self.https = https
    self.interval = interval
    self._active: bool = active
    self._logger = logging.getLogger(self.__class__.__name__)

  @property
  def active(self) -> bool:
    self._logger.info(f"Getter for _active called, active is {self._active}")
    return self._active

  @active.setter
  def active(self, active: bool):
    self._logger.info(f"Setter for _active called.")
    if active:
      self._active = active
    else:
      raise ValueError(f"Invalid value for active, got {active.lower()}, need to be true or false")

    
