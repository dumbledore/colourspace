#!/usr/bin/env python3

# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import pytest
import sys

sys.path.append("src")

if __name__ == "__main__":
    sys.exit(pytest.main(["tests"] + sys.argv[1:]))
