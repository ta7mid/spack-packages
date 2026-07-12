# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Gridpack(CMakePackage):
    """GridPACK is a high-performance computing framework for developing C++ applications
    that simulate or analyze electric power grids.

    Built on top of MPI, PETSc, ParMETIS, and Global Arrays, it provides modules for
    power-flow and dynamic simulation, contingency analysis, and state estimation, as well
    as the building blocks for developing new applications.
    """

    homepage = "https://github.com/GridOPTICS/GridPACK"
    url = "https://github.com/GridOPTICS/GridPACK/archive/refs/tags/v3.6.tar.gz"

    maintainers("ta7mid")

    version("3.6", sha256="e7170ee87c9072ff595bf2ff2db7a2bad3c7dba9ca2e4e67464b1f891839be61")

    variant("shared", default=False, description="Build as shared libraries")
    variant("progress_ranks", default=False, description="Enable progress ranks")
    variant(
        "env_from_comm",
        default=True,
        description="Enable creating GridPACK environments from communicators",
        # https://github.com/GridOPTICS/GridPACK/pull/229#pullrequestreview-2679229691
        when="^globalarrays@5.9:",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("boost@1.83: +mpi +serialization +random")
    depends_on("globalarrays +cxx")
    depends_on("mpi")
    # https://github.com/GridOPTICS/GridPACK/blob/03d41de9114e4781f1c6ac42ee0410822a0c8a4e/docs/markdown/required/PARMETIS.md?plain=1#L21
    depends_on("parmetis@4:")
    depends_on("petsc +metis +suite-sparse +superlu-dist")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        return [
            self.define("Boost_ROOT", self.spec["boost"].prefix),
            self.define("BUILD_GA", False),
            self.define("GA_DIR", self.spec["globalarrays"].prefix),
            self.define("GRIDPACK_ENABLE_TESTS", False),
            self.define("MPI_C_COMPILER", self.spec["mpi"].mpicc),
            self.define("MPI_CXX_COMPILER", self.spec["mpi"].mpicxx),
            self.define("PETSC_DIR", self.spec["petsc"].prefix),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("ENABLE_ENVIRONMENT_FROM_COMM", "env_from_comm"),
            self.define_from_variant("USE_PROGRESS_RANKS", "progress_ranks"),
        ]

    def setup_run_environment(self, env):
        env.set("GRIDPACK_DIR", self.prefix)
