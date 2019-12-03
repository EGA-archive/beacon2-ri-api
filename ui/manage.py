#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":

    os.environ.setdefault("BEACON_UI_CONF", "conf.ini")
    os.environ.setdefault("BEACON_UI_LOG", "logger.yaml")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beaconui.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

