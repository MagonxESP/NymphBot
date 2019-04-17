import json
import os
import logging


class Storage:

    def __init__(self, storage_name):
        self._storage_dir = 'data'
        self._storage_path = self._storage_dir + '/' + storage_name + '.json'
        self._storage_name = storage_name

        if os.path.isdir(self._storage_dir) is not True:
            os.mkdir(self._storage_dir)

        if os.path.isfile(self._storage_path):
            self._write({
                self._storage_name: {}
            })

    def _read(self) -> dict:
        try:
            file = open(self._storage_path, 'r')
            self.data = file.read()
            file.close()
            return json.loads(self.data)
        except IOError as e:
            logging.error(str(e))
            return {
                self._storage_name: {}
            }

    def _write(self, data):
        try:
            file = open(self._storage_path, 'w')
            file.write(json.dumps(data, indent=4))
            file.close()
        except IOError as e:
            logging.error(str(e))

    def get(self, key):
        data = self._read()
        return data[self._storage_name].get(key)

    def set(self, key, value):
        data = self._read()
        data[self._storage_name].update({key: value})
        self._write(data)
