import fnmatch
import glob
import os
import shutil
import zipfile

from no_drama.context import temp_directory
from no_drama.pip_automation import save_wheels


def inject_configuration(cli_args):
    with temp_directory() as staging_dir:
        build_zip_path = os.path.join(staging_dir, 'build.zip')

        shutil.copyfile(cli_args.build_zip, build_zip_path)

        build_zip = zipfile.ZipFile(build_zip_path, mode="a")

        # figuring out where things are in this zip file...
        all_the_wheels = fnmatch.filter(build_zip.namelist(), '*/wheels/*.whl')
        zip_wheel_dir = os.path.dirname(all_the_wheels[0])
        zip_root = os.path.normpath(os.path.join(zip_wheel_dir, '../'))

        # move just the wheels we want into the bundle dir
        wheel_destination = os.path.join(staging_dir, 'wheels')
        if cli_args.requirements_file:
            save_wheels(
                requirements_paths=[cli_args.requirements_file],
                destination=wheel_destination
            )
            wheel_pattern = os.path.join(staging_dir, 'wheels/*.whl')

            saved_wheels = glob.glob(wheel_pattern)

            for wheel_path in saved_wheels:
                name = os.path.join(
                    zip_wheel_dir, os.path.basename(wheel_path))
                build_zip.write(wheel_path, arcname=name)

        build_zip.write(
            cli_args.vars, os.path.join(
                zip_root, 'environment.json'))

        if cli_args.paths:
            build_zip.write(
                cli_args.paths, os.path.join(
                    zip_root, 'paths.d/1_custom.json'))

        if cli_args.prepend_wsgi:
            build_zip.write(cli_args.prepend_wsgi,
                            os.path.join(zip_root, 'pre-wsgi.py-fragment'))

        if cli_args.append_wsgi:
            build_zip.write(cli_args.append_wsgi,
                            os.path.join(zip_root, 'post-wsgi.py-fragment'))

        build_zip.close()
        build_filename = os.path.basename(cli_args.build_zip)
        name, ext = os.path.splitext(build_filename)
        release_filename = "%s_%s%s" % (name, cli_args.slug, ext)
        shutil.copyfile(build_zip_path, release_filename)
