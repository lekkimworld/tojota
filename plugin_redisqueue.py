from tojota import CONFIG_KEYS, MyTPlugin, Myt
from urllib.parse import urlparse
import logging
import redis
import json
import os

DEFAULT_TRIPS_QUEUE_KEY = "trips_queue"
DEFAULT_ODOMETER_QUEUE_KEY = "odometer_queue"
KEY_TOJOTA_REDIS_URL = "redis_url"
KEY_ENV_REDIS_URL = "REDIS_URL"
CONFIG_TRIPS_KEY = "redis_trips_key"
CONFIG_ODOMETER_KEY = "redis_odometer_key"

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class Plugin(MyTPlugin):
    def init(self, config_data):
        self._config_data = config_data
        redis_url_str = Myt.get_environment_or_filedata(config_data, KEY_TOJOTA_REDIS_URL)
        if (redis_url_str is None):
            log.debug("Unable to find redis url - looking for %s in environment", KEY_ENV_REDIS_URL)
            redis_url_str = os.getenv(KEY_ENV_REDIS_URL)
            log.debug("Loaded %s = %s", KEY_ENV_REDIS_URL, redis_url_str)
        redis_url = urlparse(redis_url_str)
        self._trips_key = Myt.get_environment_or_filedata(config_data, CONFIG_TRIPS_KEY) or DEFAULT_TRIPS_QUEUE_KEY
        self._odometer_key = Myt.get_environment_or_filedata(config_data, CONFIG_ODOMETER_KEY) or DEFAULT_ODOMETER_QUEUE_KEY
        self._trips_count = 0
        
        # init redis
        self._redis = redis.Redis(host=redis_url.hostname, password=redis_url.password, port=redis_url.port, db=0, decode_responses=True)

    def trip_data(self, trip_id, trip_data):
        print("Pushing trip with ID {} to redis".format(trip_id))
        json_str = json.dumps(trip_data)
        self._redis.rpush(self._trips_key, json_str)
        self._trips_count += 1

    def odometer(self, fresh, odometer, odometer_unit, fuel_percent) -> None:
        odometer_data = {
            "odometer": odometer,
            "odometer_unit": odometer_unit,
            "fuel_percent": fuel_percent
        }
        json_str = json.dumps(odometer_data)
        self._redis.rpush(self._odometer_key, json_str)
    
