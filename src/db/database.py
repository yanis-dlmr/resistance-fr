import os

import logging
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection

__all__ = ['UsefulDatabase', 'ExportUserEntry']

DB_USER = os.getenv('DB_USER', '')
DB_PASSWD = os.getenv('DB_PASSWD', '')
DB_URL = os.getenv('DB_URL', '')
DB_PORT = os.getenv('DB_PORT', None)
CONNECTION_STRING = f'mongodb+srv://{DB_USER}:{DB_PASSWD}@{DB_URL}/?retryWrites=true&w=majority'


@dataclass
class ExportUserEntry:
  """
  ## Description
  An entry of the export user list.
  """

  id: int
  xp: int


class UsefulDatabase:
  """
  ## Description
  The database class for the bot.
  """

  def __init__(self):
    self.__client: MongoClient = None
    self.log = logging.getLogger('resistance.db')

  @property
  def client(self) -> MongoClient:
    return self.__client

  @property
  def tests_collection(self) -> Collection:
    return self.client.usefull.tests

  @property
  def users_collection(self) -> Collection:
    return self.client.BDMFR.Utilisateurs

  @property
  def tasks_collection(self) -> Collection:
    return self.client.Resistance.Tasks

  @property
  def config_collection(self) -> Collection:
    return self.client.Resistance.Config

  def connect(self) -> bool:
    self.log.info('Connecting to database...')
    r = False
    if DB_USER != '' and DB_PASSWD != '':
      try:
        self.__client = MongoClient(CONNECTION_STRING, port=int(DB_PORT) if DB_PORT else None)
        self.log.info('Connected to database')
        r = True
      except Exception as e: # pylint: disable=broad-except
        self.log.error('Could not connect to database: %s', e)
    else:
      self.log.warning('No database credentials provided, skipping connection')
    return r

  def disconnect(self) -> bool:
    self.log.info('Disconnecting from database...')
    r = False
    if self.__client is not None:
      self.__client.close()
      self.__client = None
      self.log.info('Disconnected from database')
      r = True
    else:
      self.log.warning('No database connection to close')
    return r

  def test(self):
    self.log.info('Testing database connection...')
    try:
      if self.connect():
        r = self.tests_collection.insert_one({'test': 'test'})
        assert r.acknowledged and r.inserted_id is not None
        r = self.tests_collection.delete_one({'test': 'test'})
        assert r.acknowledged and r.deleted_count == 1
        self.disconnect()
      self.log.info('Test successful')
    except Exception as e: # pylint: disable=broad-except
      self.log.error('Test failed: %s', e)

  def __enter__(self) -> 'UsefulDatabase':
    self.connect()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
    self.disconnect()
    return False

  def __del__(self):
    if self.client is not None:
      self.disconnect()

  def __get_user_entry(self, user_id: int) -> dict:
    return self.users_collection.find_one({'id_user': user_id})

  def create_user(self, user_id: int, username: str) -> bool:
    """Creates a new user and returns True if the user was created"""
    if self.__get_user_entry(user_id) is not None:
      return False

    self.users_collection.insert_one({
      'id_user': user_id,
      'name_user': username,
      'XP': 0,
    })
    return True

  def add_xp_to_user(self, user_id: int, amount: int) -> int:
    """Updates user XP and return XP before update or -1 if the user does not exist"""
    if (entry := self.__get_user_entry(user_id)) is not None:
      self.users_collection.update_one(
        {'id_user': user_id},
        {'$inc': {
          'XP': entry['XP'] + amount
        }},
      )
      return entry['XP'] # return old xp
    return -1

  def get_user_xp(self, user_id: int) -> int:
    """Returns user XP or -1 if the user does not exist"""
    # BDMFR -> Utilisateurs -> {id_user, XP}
    entry = self.__get_user_entry(user_id)
    return entry['XP'] if entry is not None else -1

  def users(self) -> Generator[ExportUserEntry, None, None]:
    """Returns a generator of all users"""
    for entry in self.users_collection.find():
      yield ExportUserEntry(
        id=entry['id_user'],
        xp=entry['XP'],
      )

  def top_users(self, n: int) -> Generator[ExportUserEntry, None, None]:
    """Returns a generator of the top n users"""
    for entry in self.users_collection.find().sort('XP', -1).limit(n):
      yield ExportUserEntry(
        id=entry['id_user'],
        xp=entry['XP'],
      )

  def get_config(self) -> Generator[dict[str, Any], None, None]:
    """Returns the config"""
    for config in self.config_collection.find():
      yield config

  def get_events(self) -> Generator[dict[str, Any], None, None]:
    """Load and returns the events"""
    for task in self.tasks_collection.find():
      yield task
