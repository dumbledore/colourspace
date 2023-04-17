# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova
import av


class Container():
    def __init__(self, filename):
        self.__streams = []

    # Explicit close
    def close(self):
        pass

    # Make sure not leaking on object destruction
    def __dealloc__(self):
        self.close()

    # Context manager (with/as)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def seek(self, position=0):
        """Seek all streams to a key frame. Defaults to start of file."""

    @property
    def streams(self):
        """Returns a list of available video streams"""
        return list(self.__streams)
