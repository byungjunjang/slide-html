"""Pytest session setup for the theme-init harness.

On Windows the default locale is cp949, so a child Python spawned via
subprocess emits its stdout/stderr (and reads its files) as cp949 — while the
tests capture that output with ``encoding="utf-8"``. The mismatch raised
``UnicodeDecodeError`` on any script that prints Korean.

Forcing UTF-8 mode in the inherited environment makes every child process use
UTF-8 for both stdio and file I/O, so captured output decodes consistently
across platforms. The tests themselves already pass ``encoding="utf-8"``.
"""
import os

os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"
