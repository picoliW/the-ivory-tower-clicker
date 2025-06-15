from cx_Freeze import setup, Executable
import os
import sys

build_exe_options = {
    "packages": ["ursina", "panda3d", "direct"],
    "excludes": ["tkinter", "unittest", "email"],
    "includes": ["pkg_resources"],
    "include_files": [
        "assets/",
        "data/",
        "config.prc",
        os.path.join(sys.prefix, "Lib", "site-packages", "panda3d", "libpandagl.dll"),
        os.path.join(sys.prefix, "Lib", "site-packages", "panda3d", "libp3windisplay.dll"),
        os.path.join(sys.prefix, "Lib", "site-packages", "panda3d", "CgGL.dll"),
    ],
    "bin_includes": [
        "libpandagl.dll",
        "libp3windisplay.dll",
        "CgGL.dll"
    ],
    "optimize": 2
}

executables = [
    Executable(
        "main.py",
        base="Win32GUI" if sys.platform == "win32" else None,
        icon="assets/icon.ico",
        target_name="TheIvoryTower"
    )
]

setup(
    name="The Ivory Tower",
    version="1.0",
    description="The  Ivory Tower Clicker Game",
    options={"build_exe": build_exe_options},
    executables=executables
)