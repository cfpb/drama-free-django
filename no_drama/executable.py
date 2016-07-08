import zipfile
import os
import stat
import shutil


self_extraction_script = """
import os
import zipfile
import subprocess
import argparse

def deploy_to(deployment_dir=None):
    prefix = '%s'

    zip_path= os.path.join(os.getcwd(),__loader__.archive)
    destination = deployment_dir or os.path.dirname(zip_path)
    bundle = zipfile.ZipFile(zip_path)

    original_cwd = os.getcwd()
    os.chdir(destination)
    for member in bundle.infolist():
        filename = member.filename
        if filename.startswith(prefix) and not filename.endswith('/'):
            bundle.extract(member)

    bundle_dir = os.path.join(destination,prefix)
    activate_script = os.path.join(bundle_dir,'activate.sh')

    os.chdir(original_cwd)
    subprocess.call(['sh',activate_script])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="deploy this release")
    parser.add_argument('--destination', '-d')
    args = parser.parse_args()
    deploy_to(args.destination)
"""


def make_executable(archive_name, prefix):
    temp_name = archive_name + '_'
    shutil.move(archive_name, temp_name)
    build_zip = zipfile.ZipFile(temp_name, 'a')

    build_zip.writestr(
        '__main__.py',
        self_extraction_script %
        prefix)
    build_zip.close()

    executable_preamble = "#!/usr/bin/env python2.7\n"

    with open(archive_name, 'wb') as executable_file:
        executable_file.write(executable_preamble)
        executable_file.write(open(temp_name).read())

    exe_permissions = os.stat(archive_name)[0]
    new_permissions = exe_permissions | stat.S_IXOTH | stat.S_IXGRP | stat.S_IXUSR
    os.chmod(archive_name, new_permissions)
    os.unlink(temp_name)
