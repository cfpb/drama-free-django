import os
import pip
import hashlib



def record_req_cached(path):
    marker_path = cache_marker_for_path(path)
    if not os.path.exists('requirements_hashes'):
        os.mkdir('requirements_hashes')
    with open(marker_path, 'wb') as marker_file:
        marker_file.write('')


def save_wheels(destination, packages=[], requirements_paths=[]):
    save_wheel_command_prefix = (
        " wheel --no-deps --wheel-dir=%s" %
        destination).split()

    requirements_install_args = []

    for path in requirements_paths:
        requirements_install_args += ['-r', path]

    status = pip.main(save_wheel_command_prefix + packages + requirements_install_args)
    if status != 0:
        raise ValueError("non-zero return from pip.main() when installing")
