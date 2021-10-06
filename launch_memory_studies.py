import os

from itertools import starmap
from itertools import product
from gem5art.run import gem5Run
from gem5art.artifact import Artifact
from gem5art.tasks.tasks import run_gem5_instance

experiments_repo = Artifact.registerArtifact(
    command = """
        git clone https://github.com/mahyarsamani/memory-studies.git
    """,
    typ = "git repo",
    name = "memory-studies",
    path = "./",
    cwd = "../",
    documentation = "The repo for running the memory study experiments."
)

gem5_repo = Artifact.registerArtifact(
    command = """
        git clone https://gem5.googlesource.com/public/gem5;
        cd gem5;
        git checkout develop;
    """,
    typ = "git repo",
    name = "gem5",
    path = "gem5/",
    cwd = "./"
)

gem5_null = Artifact.registerArtifact(
    command = """
        scons build/NULL/gem5.opt -j 12;
    """,
    typ = "gem5 binary",
    name = "gem5-null",
    cwd = "gem5/",
    path = "gem5/build/NULL/gem5.opt",
    inputs = [gem5_repo],
    documentation = "gem5 binary compiled with NULL build option"
)

gem5_null_mesi_two_level = Artifact.registerArtifact(
    command = """
        scons build/NULL_MESI_Two_Level/gem5.opt -j 12;
    """,
    typ = "gem5 binary",
    name = "gem5-null-mesi-two-level",
    cwd = "gem5/",
    path = "gem5/build/NULL_MESI_Two_Level/gem5.opt",
    inputs = [gem5_repo],
    documentation = "gem5 binary compiled with NULL_MESI_Two_Level build option"
)

if __name__ == "__main__":
    generators = ["Linear", "Random"]
    cache_classes = ["NoCache", "PrivateL1", "PrivateL1PrivateL2", "MESITwoLevel"]

    def get_correct_gem5_binary(cache_class):
        if not cache_class in cache_classes:
            raise ValueError
        if cache_class == "MESITwoLevel":
            return gem5_null_mesi_two_level
        else:
            return gem5_null

    def create_run(generator, cache_class):
        gem5_binary = get_correct_gem5_binary(cache_class)
        return gem5Run.createSERun(
            name = "memory studies",
            run_script = "gem5/configs/memory_studies/memory_studies.py",
            outdir = f"results/{generator}/{cache_class}",
            gem5_artifact = gem5_binary,
            gem5_git_artifact = gem5_repo,
            run_script_git_artifact = experiments_repo,
            params =  [generator, cache_class],
            timeout = 15 * 60,
        )

    runs = starmap(create_run, product(generators, cache_classes))

    for run in runs:
        run_gem5_instance.apply_aysnc((run, os.getcwd()))
