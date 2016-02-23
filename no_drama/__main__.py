#!/usr/bin/env python

import argparse
import tempfile
import os
import os.path
import shutil
import subprocess
import zipfile
import glob
import fnmatch

from string import Template
from functools import partial


this_file = os.path.realpath(__file__)
this_directory = os.path.dirname(this_file)
templates_dir = os.path.join(this_directory, 'templates')
build_lib = os.path.join(this_directory, 'build_lib')
build_files = os.path.join(this_directory, 'build_files')


def save_wheels(destination, packages=None, requirements_file=None,
                find_links=None):
    call_list = ["pip", "wheel", "--wheel-dir=%s" % destination]

    if packages is not None:
        call_list += packages

    if find_links is not None:
        call_list += ['--find-links=%s' % find_links]

    if requirements_file is not None:
        call_list += ['-r', requirements_file]

    subprocess.call(call_list)


def get_file_from_dir(dir, filename, mode='r'):
    full_path = os.path.join(dir, filename)
    return open(full_path, mode)


def get_template(filename, mode='r'):
    template_file = get_file_from_dir(templates_dir, filename, mode=mode)
    return Template(template_file.read())

def stage_bundle(cli_args):
    staging_dir = tempfile.mkdtemp()
    build_dir = os.path.join(staging_dir, cli_args.label)

    # these are wheels needed during activation
    bootstrap_wheels = ['virtualenv','pip','wheel','distribute']
    bootstrap_wheels_destination = os.path.join(build_dir,'bootstrap_wheels')
    save_wheels(packages=bootstrap_wheels, destination=bootstrap_wheels_destination)

    # move just the wheels we want into the bundle dir  
    wheel_destination = os.path.join(build_dir, 'wheels')
    save_wheels(requirements_file = cli_args.requirements_file,
            destination= wheel_destination)

    # copy django project into bundle dir
    project_complete_path = os.path.join(os.getcwd(), cli_args.project_path)
    project_norm_path = os.path.normpath(project_complete_path)
    project_slug = os.path.basename(project_norm_path)
    project_destination = os.path.join(build_dir, project_slug)
    shutil.copytree(cli_args.project_path, project_destination)

    # make the lib directory
    destination_lib = os.path.join(build_dir, 'lib')
    shutil.copytree(build_lib, destination_lib)

    # generate the activate.sh file
    mkv_template = get_template('activate.sh.template')
    mkv_code = mkv_template.substitute(projectslug=project_slug)
    mkv_destination = os.path.join(build_dir,'activate.sh')
    with open(mkv_destination, 'wb') as mkv_outfile:
        mkv_outfile.write(mkv_code)

    wsgi_source = os.path.join(build_files, 'wsgi.py')
    wsgi_destination = os.path.join(build_dir, 'wsgi.py')
    shutil.copyfile(wsgi_source, wsgi_destination)

    archive_basename = "%s_%s" % (cli_args.name, cli_args.label)
    archive_name = shutil.make_archive(archive_basename,
                                       'zip',
                                       root_dir=staging_dir,
                                       base_dir=cli_args.label)

    print("generated build at %s" % archive_name)
    shutil.rmtree(staging_dir)
    print("deleted temporary files")


def inject_configuration(cli_args):
    staging_dir = tempfile.mkdtemp()
    build_zip_path = os.path.join(staging_dir, 'build.zip')

    shutil.copyfile(cli_args.build_zip, build_zip_path)

    build_zip = zipfile.ZipFile(build_zip_path, mode="a")

    # figuring out where things are in this zip file...
    all_the_wheels = fnmatch.filter(build_zip.namelist(), '*/wheels/*.whl')
    zip_wheel_dir = os.path.dirname(all_the_wheels[0])
    zip_root = os.path.normpath(os.path.join(zip_wheel_dir,'../'))

    # move just the wheels we want into the bundle dir
    wheel_destination = os.path.join(staging_dir, 'wheels')
    if cli_args.requirements_file:
        save_wheels(requirements_file=cli_args.requirements_file,
                    destination=wheel_destination)
        wheel_pattern = os.path.join(staging_dir, 'wheels/*.whl')

        saved_wheels = glob.glob(wheel_pattern)

        for wheel_path in saved_wheels:
            name = os.path.join(zip_wheel_dir, os.path.basename(wheel_path))
            build_zip.write(wheel_path, arcname=name)

    build_zip.write(cli_args.vars, os.path.join(zip_root, 'environment.json'))

    if cli_args.paths:
        build_zip.write(cli_args.paths, os.path.join(zip_root, 'paths.json'))

    if cli_args.append_wsgi:
        build_zip.write(cli_args.append_wsgi,
                        os.path.join(zip_root, 'extended.wsgi'))

    build_zip.close()
    build_filename = os.path.basename(cli_args.build_zip)
    name, ext = os.path.splitext(build_filename)
    release_filename = "%s_%s%s" % (name, cli_args.slug, ext)
    shutil.copyfile(build_zip_path, release_filename)


def main():
    parser = argparse.ArgumentParser(description="drama-free deployable django"
                                     " projects")

    subparsers = parser.add_subparsers()
    build_parser = subparsers.add_parser('build')
    release_parser = subparsers.add_parser('release')

    # build parser arguments
    build_parser.add_argument('project_path')
    build_parser.add_argument('requirements_file', help="just like you would"
                              " 'pip install -r'")

    build_parser.add_argument('name', help="name of this project")

    build_parser.add_argument('label', help="a label for this build-- "
                        "maybe a build ID or version number")

    build_parser.set_defaults(func=stage_bundle)

    # release parser arguments
    release_parser.add_argument('build_zip', help='path to a zip file'
                                " generated with 'no-drama build'")
    release_parser.add_argument('vars', help="JSON dictionary of env variables")
    release_parser.add_argument('slug', help="a label for this release")

    release_parser.add_argument('--paths', help="json file for overriding"
                                " default paths")
    release_parser.add_argument('--requirements_file', help="just like you would"
                        " 'pip install -r'. Let's you add more wheels to the build")

    release_parser.add_argument('--append-wsgi',
                        help="text file w/ additional python code to modify "
                        "the wsgi 'application'")

    release_parser.set_defaults(func=inject_configuration)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
