# -*- python -*-
#
# Copyright 2022 Stéphane Caron

workspace(name = "mpacklog")

BAZEL_VERSION = "4.1.0"
BAZEL_VERSION_SHA_HOST = "0eb2e378d2782e7810753e2162245ad1179c1bb12f848c692b4a595b4edf779b"
BAZEL_VERSION_SHA_PI = "02fcc51686a2f7b360a629747134d62dec885012454fac4c8634fc525884201f"

load("//tools/workspace:default.bzl", "add_default_repositories")
add_default_repositories()

# @palimpsest is a default repository
load("@palimpsest//tools/workspace:default.bzl", add_palimpsest_repositories = "add_default_repositories")
add_palimpsest_repositories()

# We can load this now that @rules_python has been added as a @palimpsest repository
load("//tools/workspace:install_python_deps.bzl", "install_python_deps")
install_python_deps()
