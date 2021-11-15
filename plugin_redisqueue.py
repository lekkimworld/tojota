from tojota import MyTPlugin, Myt
from urllib.parse import urlparse
import logging
import redis
import json
import os

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class Plugin(MyTPlugin):
    def init(self, config_data):
        self._config_data = config_data
        redis_url_str = Myt.get_environment_or_filedata(config_data, "redis_url")
        if (redis_url_str is None):
            log.debug("Unable to find redis url - looking for REDIS_URL in environment")
            redis_url_str = os.getenv("REDIS_URL")
            log.debug("Loaded REDIS_URL = %s", redis_url_str)
        redis_url = urlparse(redis_url_str)
        self._trip_key = Myt.get_environment_or_filedata(config_data, "redis_trip_key") or "trip_queue"
        self._odometer_key = Myt.get_environment_or_filedata(config_data, "redis_odometer_key") or "odometer_queue"
        
        # init redis
        self._redis = redis.Redis(host=redis_url.hostname, password=redis_url.password, port=redis_url.port, db=0, decode_responses=True)

    def trip_data(self, trip_id, trip_data):
        print("Pushing trip with ID {} to redis".format(trip_id))
        json_str = json.dumps(trip_data)
        self._redis.rpush(self._trip_key, json_str)

    def odometer(self, fresh, odometer, odometer_unit, fuel_percent) -> None:
        odometer_data = {
            "odometer": odometer,
            "odometer_unit": odometer_unit,
            "fuel_percent": fuel_percent
        }
        json_str = json.dumps(odometer_data)
        self._redis.rpush(self._odometer_key, json_str)
    
