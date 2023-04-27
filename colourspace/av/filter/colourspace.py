# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

from colourspace.av.filter import Filter

NAME = "colorspace"

# Reference: libavfilter/vf_colorspace.c: colorspace_options
# Reference: libavutil/pixfmt.h: AVColorSpace, AVColorPrimaries, AVColorTransferCharacteristic

# Note: gbr is actually AVCOL_SPC_RGB
# Unsupported colourspaces:
# AVCOL_SPC_BT2020_CL           ITU-R BT2020 constant luminance system
# AVCOL_SPC_SMPTE2085           SMPTE 2085, Y'D'zD'x
# AVCOL_SPC_CHROMA_DERIVED_NCL  Chromaticity-derived non-constant luminance system
# AVCOL_SPC_CHROMA_DERIVED_CL   Chromaticity-derived constant luminance system
# AVCOL_SPC_ICTCP               ITU-R BT.2100-0, ICtCp
COLOURSPACES = Filter.get_choices_for_option(NAME, "space")

# bt2020nc  = AVCOL_SPC_BT2020_NCL
# bt2020ncl = AVCOL_SPC_BT2020_NCL
COLOURSPACE_SYNONYMS = {
    "bt2020nc": "bt2020ncl",
}

PRIMARIES = Filter.get_choices_for_option(NAME, "primaries")

# AVCOL_PRI_JEDEC_P22 = AVCOL_PRI_EBU3213,
PRIMARY_SYNONYMS = {
    "jedec-p22": "ebu3213",
}

# Unsupported transfer characteristics:
# AVCOL_TRC_LOG             Logarithmic transfer characteristic (100:1 range)
# AVCOL_TRC_LOG_SQRT        Logarithmic transfer characteristic (100 * Sqrt(10) : 1 range)
# AVCOL_TRC_BT1361_ECG      ITU-R BT1361 Extended Colour Gamut
# AVCOL_TRC_SMPTE2084       SMPTE ST 2084 for 10-, 12-, 14- and 16-bit systems
# AVCOL_TRC_SMPTE428        SMPTE ST 428-1
# AVCOL_TRC_ARIB_STD_B67    ARIB STD-B67, known as "Hybrid log-gamma"
TRANSFERS = Filter.get_choices_for_option(NAME, "trc")


# bt470m        = AVCOL_TRC_GAMMA22
# gamma22       = AVCOL_TRC_GAMMA22
# bt470bg       = AVCOL_TRC_GAMMA28
# gamma28       = AVCOL_TRC_GAMMA28
# srgb          = AVCOL_TRC_IEC61966_2_1
# iec61966-2-1  = AVCOL_TRC_IEC61966_2_1
# xvycc         = AVCOL_TRC_IEC61966_2_4
# iec61966-2-4  = AVCOL_TRC_IEC61966_2_4
TRANSFER_SYNONYMS = {
    "bt470m": "gamma22",
    "bt470bg": "gamma28",
    "srgb": "iec61966-2-1",
    "xvycc": "iec61966-2-4",
}

RANGES = (
    "tv",  # tv/mpeg = limited
    "pc",  # pc/jpeg = full
)

PROFILE_NAMES = Filter.get_choices_for_option(NAME, "all")


class Profile:
    def __init__(self, colourspace, primaries, transfer, range=None):
        # make sure we remove any synonyms
        self.colourspace = COLOURSPACE_SYNONYMS.get(colourspace, colourspace)
        self.primaries = PRIMARY_SYNONYMS.get(primaries, primaries)
        self.transfer = TRANSFER_SYNONYMS.get(transfer, transfer)
        self.range = range

    def __eq__(self, other):
        return (self.colourspace == other.colourspace) \
            and (self.range == other.range) \
            and (self.primaries == other.primaries) \
            and (self.transfer == other.transfer)

    def __hash__(self):
        return hash(self.colourspace) \
            ^ hash(self.range) \
            ^ hash(self.primaries) \
            ^ hash(self.transfer)


PROFILES = {
    "bt470m":
        Profile("smpte170m", "bt470m", "bt470m"),
    "bt470bg":
        Profile("bt470bg", "bt470bg", "bt470bg"),
    "bt601-6-525":
        Profile("smpte170m", "smpte170m", "smpte170m"),
    "bt601-6-625":
        Profile("bt470bg", "bt470bg", "smpte170m"),
    "bt709":
        Profile("bt709", "bt709", "bt709"),
    "smpte170m":
        Profile("smpte170m", "smpte170m", "smpte170m"),
    "smpte240m":
        Profile("smpte240m", "smpte240m", "smpte240m"),
    "bt2020":
        Profile("bt2020ncl", "bt2020", "bt2020-10"),
}

DITHER = Filter.get_choices_for_option(NAME, "dither")

WHITE_POINT_ADAPTATION = Filter.get_choices_for_option(NAME, "wpadapt")


class ColourspaceFilter(Filter):
    def __init__(self, input, output, dither=None, white_point=None):
        self.input = input
        self.output = output
        self.dither = dither
        self.white_point = white_point

    @property
    def name(self):
        return NAME

    @property
    def params(self):
        params = {
            # input
            "ispace": self.input.colourspace,
            "iprimaries": self.input.primaries,
            "itrc": self.input.transfer,

            # output
            "space": self.output.colourspace,
            "primaries": self.output.primaries,
            "trc": self.output.transfer,

            # *fast* is always set to 0 (false), as it is output is useless,
            # as it is inaccurate.
            "fast": "0",
        }

        # not setting iall/all, as we specify space/primaries/trc directly

        # set optional params
        Filter.set_opt_param(params, "irange", self.input.range)
        Filter.set_opt_param(params, "range", self.output.range)
        Filter.set_opt_param(params, "dither", self.dither)
        Filter.set_opt_param(params, "wpadapt", self.white_point)

        # *format* is not supported as we are not interested in changing the frame format,
        # e.g. to yuv420p, yuv422p10, yuv444p12, etc. (all values are in YUV)

        return params
