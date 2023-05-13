# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

from colourspace.av.filter import FilteredStream
from colourspace.av.filter.colourspace import ColourspaceFilter, Profile, PROFILES
from colourspace.av.container import Container
from data import FFMPEG_FATE_FILES, LOCAL_TEST_FILES
from pymediainfo import MediaInfo


def test_stream(stream):
    stream.frame.to_image()
    print(f"... stream {stream}")


def run_test(filename):
    try:
        info = MediaInfo.parse(filename)
        if not (info.image_tracks or info.video_tracks):
            # Skip: not and image or a video
            return

        container = Container(filename)
        for stream in container.streams:
            test_stream(stream)

        # next test
        container.seek(0)

        # now test with ColourSpace
        for stream in container.streams:
            is_odd = any([x % 2 for x in (stream.width, stream.height)])
            if is_odd:
                # vf_colorspace does not support videos of odd sizes
                continue

            stream_profile, _ = Profile.from_stream(stream)
            filter = ColourspaceFilter(stream_profile, PROFILES["bt709"])
            stream = FilteredStream(stream, [filter])
            test_stream(stream)

        print(f"[P] {filename}")
    except Exception as ex:
        print(f"[F] {filename}")
        print(ex)


for filename in FFMPEG_FATE_FILES + LOCAL_TEST_FILES:
    run_test(filename)

# 1. Open Container
# 2. Stream -> Read Image
# 3. Seek
# 4. Multiple Streams
# 5. Images
# 6. Filters
