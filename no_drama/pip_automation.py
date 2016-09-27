import os
import pip
import hashlib


def hash_for_path(path):
    hasher = hashlib.sha1()
    with open(path, 'rb') as afile:
        buf = afile.read().encode('utf-8')
        hasher.update(buf)
    return hasher.hexdigest()


def cache_marker_for_path(path):
    req_hash = hash_for_path(path)
    return 'requirements_hashes/%s' % req_hash


def is_cache_update_required(path):
    marker_path = cache_marker_for_path(path)
    return not os.path.exists(marker_path)


def record_req_cached(path):
    marker_path = cache_marker_for_path(path)
    if not os.path.exists('requirements_hashes'):
        os.mkdir('requirements_hashes')
    with open(marker_path, 'wb') as marker_file:
        marker_file.write('')


def save_wheels(destination, packages=[], requirements_paths=[]):
    cache_wheel_command_prefix = "wheel --find-links=wheelhouse --wheel-dir=wheelhouse".split()
    save_wheel_command_prefix = (
        " wheel --find-links=wheelhouse --no-index --wheel-dir=%s" %
        destination).split()

    requirements_install_args = []
    requirements_cache_args = []

    record_caches = []
    for path in requirements_paths:
        requirements_install_args += ['-r', path]
        if is_cache_update_required(path):
            requirements_cache_args += ['-r', path]
            record_caches.append(path)

    status = pip.main(cache_wheel_command_prefix + packages + requirements_cache_args)
    if status != 0:
        raise ValueError("non-zero return from pip.main() when caching")

    status = pip.main(save_wheel_command_prefix + packages + requirements_install_args)
    if status != 0:
        raise ValueError("non-zero return from pip.main() when installing")

    for path in record_caches:
        record_req_cached(path)
