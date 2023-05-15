# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

from colourspace.util.path import walk_files

FFMPEG_FATE_SUITE = "../external/FFmpeg/fate-suite"

FFMPEG_FATE_SKIPPED = [
    # VQC1 supported by FFmpeg, but not by PyAV
    "vqc/samp1.avi",

    # Works with FFmpeg, but not with PyAV
    "mss2/mss2_2.wmv",

    # ffplay fails to display, but mpv works
    "svq3/svq3_decoding_regression.mov",

    # Nothing to display or corrupt
    "vp8/dash_live_video_360.hdr",
    "h264/H264_might_overflow.mkv",
    "h264-conformance/FM1_BT_B.h264",
    "h264-conformance/FM2_SVA_B.264",
    "h264-conformance/FM2_SVA_C.264",
    "hevc-conformance/TSUNEQBD_A_MAIN10_Technicolor_2.bit",
    "mov/mov-tenc-only-encrypted.mp4",
    "mov/mov-3elist-encrypted.mov",
    "mov/mp4-with-mov-in24-ver.mp4",
    "mpegts/pmtchange.ts",

    # Seeking fails with av.error.PermissionError
    "sipr/sipr_5k0.rm",

    # IMF not supported
    "imf/countdown/ASSETMAP.xml",
    "imf/countdown/PKL_c8f6716b-0dfa-4062-8569-98fc77637287.xml",
    "imf/countdown/CPL_bb2ce11c-1bb6-4781-8e69-967183d02b9b.xml",
    "imf/countdown-audio/ASSETMAP.xml",
    "imf/countdown-audio/PKL_32a1eb00-4e39-483b-98f6-8e4086379d3c.xml",
    "imf/countdown-audio/CPL_688f4f63-a317-4271-99bf-51444ff39c5b.xml",

    # Do not work with Filters
    "h264-conformance/CVFC1_Sony_C.jsv",
    "hevc-conformance/CONFWIN_A_Sony_1.bit",
    "h264/extradata-reload-multi-stsd.mov",

    # Format not supported (F32)
    "tiff/lzw_rgbf32le.tif",
    "tiff/uncompressed_rgbf32le.tif",
    "tiff/zip_rgbf32le.tif",
    "tiff/lzw_rgbaf32le.tif",
    "tiff/zip_rgbaf32le.tif",
    "tiff/uncompressed_rgbaf32le.tif",
]

FFMPEG_FATE_FILES = walk_files(FFMPEG_FATE_SUITE, FFMPEG_FATE_SKIPPED)

LOCAL_TEST_SUITE = "../data/"
LOCAL_TEST_FILES = walk_files(LOCAL_TEST_SUITE)
