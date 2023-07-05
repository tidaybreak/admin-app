__author__ = 'Ti'

from app.services.base import BaseService
from app.utils import utils as utils
from app.utils.ciopaas import ciopaas as ciopaaas
from app.jobs.aicrm import fun_dailtask
from app.ext import serv, cache
from app.config import cfg
import datetime, os, time


class BusPhoneService(BaseService):
    def __init__(self):
        super(BusPhoneService, self).__init__()
