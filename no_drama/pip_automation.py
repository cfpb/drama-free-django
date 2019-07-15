import os
import subprocess


def save_wheels(pythons, destination, packages=[], requirements_paths=[]):
    """Collect Python wheels for all packages and requirements.

    Given a list of packages and requirements files, invoke "pip wheel" to
    download and/or create wheels for each of them, storing them in the
    specified destination directory.
    """

    # Call pip externally using this command:
    #
    # python -m pip wheel --wheel-dir=dest p1 p2 p3 -r req1.txt -r req2.txt
    # https://pip.pypa.io/en/stable/user_guide/#using-pip-from-your-program
    environment = os.environ.copy()

    for python in pythons:
        subprocess.check_call(
            [python['name'], '-m', 'pip'] +
            ['wheel', '--wheel-dir=%s' % destination,
            '--find-links=%s' % destination] +
            packages +
            ['-r' + path for path in requirements_paths],
            env=environment
        )



