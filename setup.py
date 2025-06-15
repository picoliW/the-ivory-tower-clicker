from cx_Freeze import setup, Executable
import os
import sys

if sys.platform == "linux":
    panda3d_libs = [
        os.path.join(sys.prefix, "lib", f"libpanda{lib}.so")
        for lib in ["", "express", "gl", "physics", "direct"]
    ]
    panda3d_libs = [lib for lib in panda3d_libs if os.path.exists(lib)]
    
    include_files = [
        "assets/",
        "data/",
        "config.prc",
        *panda3d_libs
    ]
    
    bin_includes = []
else:
    include_files = [
        "assets/",
        "data/",
        "config.prc",
        os.path.join(sys.prefix, "Lib", "site-packages", "panda3d", "libpandagl.dll"),
        os.path.join(sys.prefix, "Lib", "site-packages", "panda3d", "libp3windisplay.dll"),
        os.path.join(sys.prefix, "Lib", "site-packages", "panda3d", "CgGL.dll"),
    ]
    bin_includes = [
        "libpandagl.dll",
        "libp3windisplay.dll",
        "CgGL.dll"
    ]

build_exe_options = {
    "packages": ["ursina", "panda3d", "direct"],
    "excludes": ["tkinter", "unittest", "email"],
    "includes": ["pkg_resources"],
    "include_files": include_files,
    "bin_includes": bin_includes,
    "optimize": 2
}

executables = [
    Executable(
        "main.py",
        base=None,  
        icon="assets/icon.png" if sys.platform == "linux" else "assets/icon.ico",
        target_name="TheIvoryTower"
    )
]

setup(
    name="The Ivory Tower",
    version="1.0",
    description="The Ivory Tower Clicker Game",
    options={"build_exe": build_exe_options},
    executables=executables
)