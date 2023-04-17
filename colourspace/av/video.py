# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova
from colourspace.av.stream import Stream


class VideoStream(Stream):
    def __init__(self, container, raw_container, stream):
        self.__container = container
        self.__raw_container = raw_container
        self.__stream = stream
        self.__frame = None

    def __get_frame(self, position):
        # Crude seek to a key frame
        self.__container.seek(position)

        # Now seek to a fine position, not just a keyframe
        # by decoding frames until reaching the correct position

        # Keep a copy of the previously decoded frame as it will be the last frame
        # before overrunning the position being sought, thus the correct frame to return
        previous_video_frame = None

        # Demux the container and get the next pack for this video stream
        for packet in self.__raw_container.demux(self.__stream):
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
        self.__frame = self.__get_frame(position)

    def frame(self):
        """Obtains the current frame"""
        return self.__frame
