# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import av

from colourspace.av.video import VideoStream


class Container():
    def __init__(self, filename):
        container = av.open(filename)
        self._container = container
        self._streams = [VideoStream(self, v) for v in container.streams.video]

    # Explicit close
    def close(self):
        """Close the container resource"""
        self._container.close()

    # Make sure not leaking on object destruction
    def __dealloc__(self):
        self.close()

    # Context manager (with/as)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def filename(self):
        """Returns the filename of the container"""
        return self._container.name

    def seek(self, position=0):
        """Seek all streams to a key frame. Defaults to start of file."""

        # Convert to US
        position = int(position * av.time_base)

        # Seek entire container (all streams) to a key frame
        self._container.seek(position)

    @property
    def streams(self):
        """Returns a list of available video / image streams"""
        return list(self._streams)
