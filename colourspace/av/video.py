# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

from colourspace.av.stream import Stream


class VideoStream(Stream):
    def __init__(self, container, stream):
        self._container = container
        self._stream = stream
        self._frame = self._get_frame()
        self._position = 0
        self._key_frames = [float(p.pts * p.time_base)
                            for p in stream.container.demux(stream) if p.is_keyframe]
        # rewind container
        container.seek(0)

    def _get_frame(self, position=0):
        # Crude seek to a key frame
        self._container.seek(position)

        # Now seek to a fine position, not just a keyframe
        # by decoding frames until reaching the correct position

        # Keep a copy of the previously decoded frame as it will be the last frame
        # before overrunning the position being sought, thus the correct frame to return
        previous_video_frame = None

        # Demux the container and get the next pack for this video stream
        for packet in self._stream.container.demux(self._stream):
            # Decode all frames in this packet that we just demuxed
            for frame in packet.decode():
                # Convert the decoded frame postion to seconds
                frame_pos = float(frame.pts * frame.time_base)

                if frame_pos > position:
                    # This frame is JUST pass the position in time
                    # Return the previously devode frame, or this one if
                    # it was the first one anyway
                    return previous_video_frame if previous_video_frame else frame

                # Cache this current frame
                previous_video_frame = frame

        # no more frames (EOF), return whatever was last
        return previous_video_frame

    def seek(self, position=0):
        """Seek to a precise position. Defaults to start of file."""
        # Actually seek only if position has changed or decoding for the first time
        if position != self._position or not self._frame:
            self._position = position
            self._frame = self._get_frame(position)
            return True

        # No need to seek
        return False

    @property
    def frame(self):
        """Returns the current frame"""
        return self._frame

    @property
    def container(self):
        """Returns the file container"""
        return self._container

    @property
    def width(self):
        """Returns the width of the video frames"""
        return self._stream.width

    @property
    def height(self):
        """Returns the width of the height frames"""
        return self._stream.height

    @property
    def duration(self):
        """Returns the duration of the stream in seconds"""
        return float(self._stream.duration * self._stream.time_base)

    @property
    def key_frames(self):
        """Returns a list of the positions of the keyframes"""
        return list(self._key_frames)
