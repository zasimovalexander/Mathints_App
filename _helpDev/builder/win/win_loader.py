"""
Entry-point loader uses a named mutex to prevent multiple application instances.
"""


from win32event import CreateMutex
from win32api import GetLastError
from winerror import ERROR_ALREADY_EXISTS
from sys import exit


app_mutex = CreateMutex(None, False, "Mathints_single_instance")  # must be on the module's global level
if GetLastError() == ERROR_ALREADY_EXISTS:
    exit()


import conductor
conductor.ui_pick()
