import json
from tojota import MyTPlugin

class Plugin(MyTPlugin):
    def init(self, config_data):
        # noop
        self._config_data = config_data
        self._trips = 0
    
    def trip_data(self, trip_id, trip_data):
        json_str = json.dumps(trip_data)
        print(json_str)
        self._trips += 1
    
    def trip_data_done(self):
        print("Processed {} trips".format(self._trips))
    
