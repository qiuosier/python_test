import os
import re
import shlex
import subprocess
import sys
import time
from mlflow.cli import cli

from ads.jobs.templates.driver_oci import GitManager, GitJobRunner


CONST_ENV_GIT_URL = "GIT_URL"
CONST_ENV_GIT_BRANCH = "GIT_BRANCH"
CONST_ENV_GIT_COMMIT = "GIT_COMMIT"
CONST_ENV_CONDA_YAML = "CONDA_YAML"


def run_command(command: str, conda: str = None) -> int:
    """Runs a shell command.

    Returns
    -------
    int
        The return code of the command.
    """
    print(">>> %s", command)
    if conda:
        # Conda activate
        # https://docs.conda.io/projects/conda/en/latest/release-notes.html#id241
        cmd = (
            "CONDA_BASE=$(conda info --base) && "
            + "source $CONDA_BASE/etc/profile.d/conda.sh && "
            + f"conda activate {conda}; "
            + command # python script.py
        )
    else:
        cmd = command
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),
        shell=True,
    )
    # Stream the outputs
    while True:
        output = process.stdout.readline()
        if process.poll() is not None and output == b"":
            break
        if output:
            msg = output.decode()
            # output already contains the line break
            print(msg, flush=True, end="")

        # Add a small delay so that
        # outputs will have different timestamp for oci logging
        time.sleep(0.01)
    return process.returncode


def main():
    git_uri = None
    git_path = None
    for arg in sys.argv:
        match = re.match(r"(https?:\/\/.*\.git)#?(.*)", arg)
        if not match:
            continue
        git_uri, git_path = match.groups()
        print(f"Git URI: {git_uri}")
        print(f"Path: {git_path}")
        break

    if CONST_ENV_GIT_URL in os.environ or git_uri:
        git_manager = (
            GitManager(os.environ.get(CONST_ENV_GIT_URL, git_uri))
            .fetch_repo()
            .checkout_code(
                branch=os.environ.get(CONST_ENV_GIT_BRANCH),
                commit=os.environ.get(CONST_ENV_GIT_COMMIT),
            )
        )

        GitJobRunner(git_manager).set_working_dir()
        conda_prefix = "mlflow_env"

        if CONST_ENV_CONDA_YAML in os.environ:

            conda_yaml = os.environ[CONST_ENV_CONDA_YAML]

            if git_path and not os.path.exists(conda_yaml):
                conda_yaml = os.path.join(git_path, conda_yaml)
            if os.path.exists(conda_yaml):
                cmd = f"conda env create --name {conda_prefix} --file {conda_yaml}"
                run_command(cmd)
                sys.argv.append("--env-manager=local")
            else:
                print(f"File not found: {conda_yaml}")
    else:
        conda_prefix = sys.executable.split("/bin/python", 1)[0]

    run_command(shlex.join(sys.argv[1:]), conda=conda_prefix)


if __name__ == "__main__":
    main()
