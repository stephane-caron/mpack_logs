# -*- python -*-
#
# Copyright 2022 Stéphane Caron

load("@rules_python//python:pip.bzl", "pip_install")

def install_python_deps():
    """
    Install Python packages to a @pip_mpacklog external repository.

    This function intended to be loaded and called from your WORKSPACE.
    """
    pip_install(
        name = "pip_mpacklog",
        requirements = Label("//tools/workspace/pip_mpacklog:requirements.txt"),
    )
