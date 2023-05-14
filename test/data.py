# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

from colourspace.util.path import walk_files

FFMPEG_FATE_SUITE = "../external/FFmpeg/fate-suite"
FFMPEG_FATE_FILES = walk_files(FFMPEG_FATE_SUITE)

LOCAL_TEST_SUITE = "../data/"
LOCAL_TEST_FILES = walk_files(LOCAL_TEST_SUITE)
