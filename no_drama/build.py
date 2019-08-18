import json
import glob
import os
import os.path
import shutil

from pip._internal import wheel
from no_drama.context import temp_directory
from no_drama.executable import make_executable
from no_drama.pip_automation import save_wheels


this_file = os.path.realpath(__file__)
this_directory = os.path.dirname(this_file)
build_skel = os.path.join(this_directory, 'build_skel')


def wheel_tags_iterator(wheel_name):
    py_tags, abi_tags, platform_tags= (wheel_name.split('-')[-3:])
    for py_tag in py_tags.split('.'):
        for abi_tag in abi_tags.split('.'):
            for platform_tag in platform_tags.split('.'):
                yield [py_tag,abi_tag,platform_tag]


def supported_wheels_filter(wheel_paths, supported_tags):
    return [path for path in wheel_paths if wheel.Wheel(
        path).supported(tags=supported_tags)]

def stage_bundle(cli_args):
    archive_basename = "%s_%s" % (cli_args.name, cli_args.label)
    executable_path = os.path.join(os.getcwd(), archive_basename + '.zip')

    if os.path.exists(executable_path) and not cli_args.f:
        print("%s already exists, skipping. Call with -f to force rebuild" % (
            executable_path
        ))
        return

    with temp_directory() as staging_dir:
        build_dir = os.path.join(staging_dir, cli_args.label)

        shutil.copytree(build_skel, build_dir)

        # these are wheels needed during activation
        bootstrap_wheels = ['virtualenv', 'pip', 'setuptools', 'wheel']
        bootstrap_wheels_destination = os.path.join(
            build_dir, 'bootstrap_wheels')
        save_wheels(cli_args.python, packages=bootstrap_wheels,
                    destination=bootstrap_wheels_destination)

        # move just the wheels we want into the bundle dir
        wheel_destination = os.path.join(
            build_dir, 'wheels')


        if cli_args.r:
            save_wheels(
                cli_args.python,
                destination=wheel_destination,
                requirements_paths=cli_args.r)

        wheels = glob.glob(
            os.path.join(wheel_destination, '*.whl'))

        # write a requirements file for each python version
        for python in cli_args.python:
            requirements_file_path = os.path.join(
                build_dir,'requirements-%s.txt' % python['slug'])
            compatible_wheels = supported_wheels_filter(wheels, python['supported_tags'])
            reqlines = [os.path.relpath(p, build_dir) + '\n' for p in compatible_wheels]
            with open(requirements_file_path, 'wb') as reqfile:
                reqfile.writelines(reqlines)

        # copy django project into bundle dir
        project_complete_path = os.path.join(
            os.getcwd(), cli_args.project_path)
        project_norm_path = os.path.normpath(project_complete_path)
        project_slug = os.path.basename(project_norm_path)
        project_destination = os.path.join(build_dir, project_slug)
        shutil.copytree(cli_args.project_path, project_destination)

        # install paths.d/0_build.json, so activate.sh can find the django_root
        paths_d = os.path.join(build_dir, 'paths.d')
        initial_paths_path = os.path.join(paths_d, '0_build.json')

        with open(initial_paths_path, 'w') as initial_paths_file:
            json.dump({'django_root': project_slug}, initial_paths_file)

        if cli_args.static:
            for index, path in enumerate(cli_args.static):
                destination = os.path.join(build_dir, 'static.in/%s/' % index)
                shutil.copytree(path, destination)

        if cli_args.aux:
            aux_root = os.path.join(build_dir, 'aux')
            for aux_spec in cli_args.aux:
                if '=' in aux_spec:
                    slug, src = aux_spec.split('=')
                else:
                    # normalize the path, so that it  will not end in a /
                    # required for basename to get the last path component
                    # would auth_path.split('/')[-1] be simpler? maybe.
                    norm_path = os.path.normpath(aux_spec)
                    slug = os.path.basename(norm_path)
                    src = aux_spec

                destination = os.path.join(aux_root, slug)
                shutil.copytree(src, destination)

        archive_name = shutil.make_archive(archive_basename,
                                           'zip',
                                           root_dir=staging_dir,
                                           base_dir=cli_args.label)

        make_executable(archive_name, prefix=cli_args.label)
        print("generated build at %s" % executable_path)
