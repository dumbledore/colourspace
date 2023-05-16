# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import pytest

from colourspace.av.filter import FilteredStream
from colourspace.av.filter.colourspace import ColourspaceFilter, Profile, PROFILES
from colourspace.av.container import Container
from data import TEST_INFOS


def check_stream(stream):
    stream.frame.to_image()
    stream.seek(stream.duration / 2)
    stream.frame.to_image()


@pytest.mark.parametrize("filename, info", TEST_INFOS.items())
def test_av(filename, info):
    container = Container(filename)

    for stream in container.streams:
        check_stream(stream)

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
        check_stream(stream)
