# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import av

from colourspace.av.video import VideoStream
from pymediainfo import MediaInfo


class Container():
    def __init__(self, filename):
        container = av.open(filename)
        info = MediaInfo.parse(filename)

        # If it has image tracks, we treat it as an image-only
        # and observe only those tracks. This is necessary as in PyAV
        # there are no image tracks, only video tracks, and images simply
        # use the video tracks
        tracks = info.image_tracks if info.image_tracks else info.video_tracks

        # If there is only one track, disregard the ID.
        # This is needed for images, as there is only one image track
        # with an id of 'None'.
        if (len(tracks) == 1) and (len(container.streams.video) == 1):
            streams = [(container.streams.video[0], tracks[0])]
        else:
            # Multiple tracks require matching the track IDs
            # Reshape the tracks into a {id: track}
            tracks = {t.track_id: t for t in tracks}

            # now create the (stream, track) pairs
            streams = [(v, tracks[v.id]) for v in container.streams.video]

        self._container = container

        # Videos without a duration and images are not seekable
        self._seekable = bool(container.duration) and any(
            True for v, i in streams if i.track_type == "Video")

        self._streams = [VideoStream(self, v, vars(i)) for v, i in streams]

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

        # Only seek for seekable containers. Otherwise FFmpeg may return
        # 'operation not supported'.
        if self.seekable:
            # Convert to US
            position = int(position * av.time_base)

            # Seek entire container (all streams) to a key frame
            self._container.seek(position)

    @property
    def seekable(self):
        """Returns true if the container is seekable (contains a proper video)"""
        return self._seekable

    @property
    def streams(self):
        """Returns a list of available video / image streams"""
        return list(self._streams)
