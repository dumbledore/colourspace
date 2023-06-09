#!/usr/bin/env python3

# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import logging
import pytest
import sys

sys.path.append("src")

if __name__ == "__main__":
    # 2023-06-10 01:03:53,653 66713 WARNING libav.swscaler video.py:28: deprecated pixel format used, make sure you did set range correctly
    format = "%(asctime)s %(process)d %(levelname)s %(name)s %(filename)s:%(lineno)d: %(message)s"
    logging.basicConfig(format=format)

    sys.exit(pytest.main(["tests"] + sys.argv[1:]))
