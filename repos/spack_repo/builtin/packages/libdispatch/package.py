# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Libdispatch(CMakePackage):
    """libdispatch is a low-level user space library that provides uniform and comprehensive
    support for concurrent code execution to C and Swift programs across all Swift platforms.  It
    serves as the core implementation of Grand Central Dispatch (GCD), the programming framework
    designed by Apple to optimize and simplify multithreaded programming on modern multicore
    hardware."""

    homepage = "https://swiftlang.github.io/swift-corelibs-libdispatch/"
    url = "https://github.com/swiftlang/swift-corelibs-libdispatch/archive/refs/tags/swift-6.1.1-RELEASE.tar.gz"

    license("Apache-2.0", checked_by="ta7mid")

    version("6.1.1", sha256="6fc6f8b1767a1348e1d960647b2bfbc52fd7074b7aeab97bd0f4b21af58baa47")
    version("6.1", sha256="5bba8d7442890f7dbd37a9245340c5bb0c4c924dee6180ba30385b24e3fdf121")
    version("6.0.3", sha256="444c0de5fe18e148548a3f3b60b3bac3d4d586285c21064346c7ca17ed1d4fac")

    variant("shared", default=True, description="Build shared libraries")
    variant("dtrace", default=False, description="Enable DTrace support")
    variant("init_ctor", default=True, description="Enable libdispatch_init as a constructor")
    variant(
        "thread_local",
        default=True,
        description="Enable use of thread-local storage via _Thread_local",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # FIXME: Add dependencies if required.
    # depends_on("foo")

    def url_for_version(self, version):
        return f"https://github.com/swiftlang/swift-corelibs-libdispatch/archive/refs/tags/swift-{version}-RELEASE.tar.gz"

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("ENABLE_DTRACE", "dtrace"),
            self.define_from_variant("ENABLE_DISPATCH_INIT_CONSTRUCTOR", "init_ctor"),
            self.define_from_variant("ENABLE_THREAD_LOCAL_STORAGE", "thread_local"),
        ]
        return args
