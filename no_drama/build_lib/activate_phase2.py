import os

from dfd_paths import root, update_symlink

if update_symlink:
    if os.path.exists(update_symlink):
        os.remove(update_symlink)
    os.symlink(root, update_symlink)
