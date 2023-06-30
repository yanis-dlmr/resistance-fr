import os

from typing import Generator
from dataclasses import dataclass

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from ..helper.logger import logger as log

__all__ = ['UsefulDatabase', 'ExportUserEntry']

DB_USER = os.getenv('DB_USER', '')
DB_PASSWD = os.getenv('DB_PASSWD', '')
CONNECTION_STRING = f'mongodb+srv://{DB_USER}:{DB_PASSWD}@cluster0.3sxzq.mongodb.net/?retryWrites=true&w=majority'


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
    ...

  def connect(self) -> bool:
    log.debug('Connecting to database...')
    r = False
    if DB_USER != '' and DB_PASSWD != '':
      try:
        self.__client = MongoClient(CONNECTION_STRING)
        log.debug('Connected to database')
        r = True
      except Exception as e:
        log.error(f'Could not connect to database: {e}')
    else:
      log.warning('No database credentials provided, skipping connection')
    return r

  def disconnect(self) -> bool:
    log.debug('Disconnecting from database...')
    r = False
    if self.__client is not None:
      self.__client.close()
      self.__client = None
      log.debug('Disconnected from database')
      r = True
    else:
      log.warning('No database connection to close')
    return r

  def test(self):
    log.info('Testing database connection...')
    try:
      if self.connect():
        self.tests_collection.insert_one({'test': 'test'})
        self.tests_collection.delete_one({'test': 'test'})
        self.disconnect()
      log.info('Test successful')
    except Exception as e:
      log.error(f'Test failed: {e}')

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
    entry = self.__get_user_entry(user_id)
    if entry is not None:
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
