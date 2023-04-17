# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

class Stream():
    def seek(self, position=0):
        """Seek to a precise position. Defaults to start of file."""
        raise NotImplementedError()

    def frame(self):
        """Obtains the current frame"""
        raise NotImplementedError()
