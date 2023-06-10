# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import os
import pytest

from colourspace.util.settings import Settings

FILENAME = "test.pkl"


def remove_file(filename):
    try:
        os.remove(filename)
    except:
        pass


def setup_function():
    remove_file(FILENAME)


def teardown_function():
    remove_file(FILENAME)


def test_read_one_from_empty():
    settings = Settings(FILENAME)
    # Reading from an empty file must return default
    assert settings.get("test1", 123) == 123


def test_save_one_read_default():
    settings = Settings(FILENAME)
    settings.set("test2", "something")
    # Reading from a non-empty file without the setting
    # must return the default
    assert settings.get("test1", 123) == 123


def test_save_two_read_one():
    settings = Settings(FILENAME)
    # Add the setting and some other setting
    settings.set("test1", "something")
    settings.set("test2", "other")
    assert settings.get("test1", 123) == "something"


def test_remove_one_from_empty():
    settings = Settings(FILENAME)
    settings.remove("test1")


def test_save_two_remove_one_get_one_default():
    settings = Settings(FILENAME)
    # Add the setting and some other setting
    settings.set("test1", "something")
    settings.set("test2", "other")
    settings.remove("test2")
    assert settings.get("test2", 123) == 123
