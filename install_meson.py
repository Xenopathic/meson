#!/usr/bin/env python3

# Copyright 2013-2014 Jussi Pakkanen

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script installs Meson. We can't use Meson to install itself
# because of the bootstrap problem. We can't use any other build system
# either becaust that would be just silly.

import os, sys, glob, shutil, gzip
from optparse import OptionParser

usage_info = '%prog [--prefix PREFIX] [--destdir DESTDIR]'

parser = OptionParser(usage=usage_info)

parser.add_option('--prefix', default='/usr/local', dest='prefix',
                  help='the installation prefix (default: %default)')
parser.add_option('--destdir', default='', dest='destdir',
                  help='the destdir (default: %default)')

(options, args) = parser.parse_args(sys.argv)
if options.prefix[0] != '/':
    print('Error, prefix must be an absolute path.')
    sys.exit(1)

if options.destdir == '':
    install_root = options.prefix
else:
    install_root = os.path.join(options.destdir, options.prefix[1:])

script_dir = os.path.join(install_root, 'share/meson')
bin_dir = os.path.join(install_root, 'bin')
bin_script = os.path.join(script_dir, 'meson.py')
gui_script = os.path.join(script_dir, 'mesongui.py')
conf_script = os.path.join(script_dir, 'mesonconf.py')
bin_name = os.path.join(bin_dir, 'meson')
gui_name = os.path.join(bin_dir, 'mesongui')
conf_name = os.path.join(bin_dir, 'mesonconf')
man_dir = os.path.join(install_root, 'share/man/man1')
in_manfile = 'man/meson.1'
out_manfile = os.path.join(man_dir, 'meson.1.gz')
in_guimanfile = 'man/mesongui.1'
out_guimanfile = os.path.join(man_dir, 'mesongui.1.gz')
in_confmanfile = 'man/mesonconf.1'
out_confmanfile = os.path.join(man_dir, 'mesonconf.1.gz')

symlink_value = os.path.relpath(bin_script, os.path.dirname(bin_name))
guisymlink_value = os.path.relpath(gui_script, os.path.dirname(gui_name))
confsymlink_value = os.path.relpath(conf_script, os.path.dirname(conf_name))
files = glob.glob('*.py')
files += glob.glob('*.ui')

noinstall = ['compile_meson.py', 'install_meson.py', 'run_tests.py', 'run_cross_test.py']

files = [x for x in files if x not in noinstall]

os.makedirs(script_dir, exist_ok=True)
os.makedirs(bin_dir, exist_ok=True)
os.makedirs(man_dir, exist_ok=True)

for f in files:
    print('Installing %s to %s.' %(f, script_dir))
    outfilename = os.path.join(script_dir, f)
    shutil.copyfile(f, outfilename)
    shutil.copystat(f, outfilename)
try:
    os.remove(bin_name)
except OSError:
    pass
print('Creating symlinks %s and %s.' % (bin_name, gui_name))
try:
    os.unlink(bin_name)
except FileNotFoundError:
    pass
try:
    os.unlink(gui_name)
except FileNotFoundError:
    pass
try:
    os.unlink(conf_name)
except FileNotFoundError:
    pass
os.symlink(symlink_value, bin_name)
os.symlink(guisymlink_value, gui_name)
os.symlink(confsymlink_value, conf_name)
print('Installing manfiles to %s.' % man_dir)
open(out_manfile, 'wb').write(gzip.compress(open(in_manfile, 'rb').read()))
open(out_confmanfile, 'wb').write(gzip.compress(open(in_confmanfile, 'rb').read()))
open(out_guimanfile, 'wb').write(gzip.compress(open(in_guimanfile, 'rb').read()))
