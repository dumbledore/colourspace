# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

from colourspace.util.path import walk_files
from pymediainfo import MediaInfo
from subprocess import check_call

FFMPEG_FATE_SUITE_URL = "rsync://fate-suite.ffmpeg.org/fate-suite/"

FFMPEG_FATE_SUITE = "testdata"

FFMPEG_FATE_SKIPPED = [
    # VQC1 supported by FFmpeg, but not by PyAV
    "vqc/samp1.avi",

    # Works with FFmpeg, but not with PyAV
    "mss2/mss2_2.wmv",

    # ffplay fails to display, but mpv works
    "svq3/svq3_decoding_regression.mov",

    # Nothing to display or corrupt
    "h264-conformance/FM1_BT_B.h264",
    "h264-conformance/FM2_SVA_B.264",
    "h264-conformance/FM2_SVA_C.264",
    "h264/H264_might_overflow.mkv",
    "hevc-conformance/TSUNEQBD_A_MAIN10_Technicolor_2.bit",
    "mov/mov-3elist-encrypted.mov",
    "mov/mov-tenc-only-encrypted.mp4",
    "mov/mp4-with-mov-in24-ver.mp4",
    "mpegts/pmtchange.ts",
    "vp8/dash_live_video_360.hdr",

    # Seeking fails with av.error.PermissionError
    "sipr/sipr_5k0.rm",

    # IMF not supported
    "imf/countdown-audio/ASSETMAP.xml",
    "imf/countdown-audio/CPL_688f4f63-a317-4271-99bf-51444ff39c5b.xml",
    "imf/countdown-audio/PKL_32a1eb00-4e39-483b-98f6-8e4086379d3c.xml",
    "imf/countdown/ASSETMAP.xml",
    "imf/countdown/CPL_bb2ce11c-1bb6-4781-8e69-967183d02b9b.xml",
    "imf/countdown/PKL_c8f6716b-0dfa-4062-8569-98fc77637287.xml",

    # Do not work with Filters
    "h264-conformance/CVFC1_Sony_C.jsv",
    "h264/extradata-reload-multi-stsd.mov",
    "hevc-conformance/CONFWIN_A_Sony_1.bit",

    # Format not supported (F32)
    "tiff/lzw_rgbaf32le.tif",
    "tiff/lzw_rgbf32le.tif",
    "tiff/uncompressed_rgbaf32le.tif",
    "tiff/uncompressed_rgbf32le.tif",
    "tiff/zip_rgbaf32le.tif",
    "tiff/zip_rgbf32le.tif",

    # Frame size change (not going to support it)
    "dpx/lena_4x_concat.dpx",
    "hevc/extradata-reload-multi-stsd.mov",
    "vp8/frame_size_change.webm",
    "vp9-test-vectors/vp90-2-05-resize.ivf",

    # Do not work on Linux
    "mkv/prores_bz2.mkv",

    # Pixel format 0x11311100 bits:8 is not implemented.
    # No support in PyAV which uses FFmpeg 5.1.2, but it is only
    # present on FFmpeg master anyway. Check 0b352e350e7.
    "jpg/jpg-8930-2.jpg",
    "jpg/jpg-8930-4.jpg",
    "jpg/jpg-8930-5.jpg",
]

# Make sure it is rsynced
# Check fate-rsync target in FFmpeg/tests/Makefile
check_call([
    "rsync",
    "-vrltLW", "--timeout=60",
    FFMPEG_FATE_SUITE_URL, FFMPEG_FATE_SUITE
])

FFMPEG_FATE_FILES = walk_files(FFMPEG_FATE_SUITE, FFMPEG_FATE_SKIPPED)

# Generate all infos
ALL_INFOS = {filename: MediaInfo.parse(filename)
             for filename in FFMPEG_FATE_FILES}

# Select only images or videos
TEST_INFOS = {filename: info for filename, info in ALL_INFOS.items()
              if info.image_tracks or info.video_tracks}
