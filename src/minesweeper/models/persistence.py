from abc import ABC, abstractmethod
import json
import os
import pickle


class Persistence(ABC):
    """An abstract class that defines the interface for a persistence class"""

    @abstractmethod
    def dump(self, data):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def is_file_exists(self) -> bool:
        pass


class JsonPersistence(Persistence):
    """A persistence class that saves and loads data to a JSON"""

    FILE_NAME = "data.json"

    def dump(self, data):
        with open(self.FILE_NAME, "w") as jsonfile:
            json.dump(data, jsonfile)

    def load(self):
        try:
            with open(self.FILE_NAME) as jsonfile:
                return json.load(jsonfile)
        except Exception as ex:
            print("Error loading file", ex)
            return []

    def is_file_exists(self) -> bool:
        return os.path.exists(self.FILE_NAME) and os.path.isfile(self.FILE_NAME)


class PicklePersistence(Persistence):
    """A persistence class that saves and loads data to a JSON"""

    FILE_NAME = "data.pickle"

    def dump(self, data):
        with open(self.FILE_NAME, "wb") as f:
            pickle.dump(data, f)

    def load(self):
        with open(self.FILE_NAME, "rb") as f:
            return pickle.load(f)

    def is_file_exists(self) -> bool:
        return os.path.exists(self.FILE_NAME) and os.path.isfile(self.FILE_NAME)


class PersistenceMock(Persistence):
    """A mock persistence class used for testing"""

    def dump(self, data):
        pass

    def load(self):
        pass

    def is_file_exists(self) -> bool:
        return False
