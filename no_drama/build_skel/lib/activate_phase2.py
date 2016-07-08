import os

from dfd import root, get_path

update_symlink = get_path('update_symlink')
if update_symlink:
    if os.path.exists(update_symlink):
        os.remove(update_symlink)
    os.symlink(root, update_symlink)
