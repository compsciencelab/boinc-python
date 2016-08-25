#!/usr/bin/env python2

from __future__ import print_function

import os
import re
# Get slot dir
cwd = os.getcwd()

slot = "0"
if re.match( "^.*/slot-[0-9]*$", cwd ):
  slot = re.sub( "^.*/slot-", "", cwd );

home =os.path.expanduser("~")
install_dir = os.path.join( home, ".gpugrid", "slot-" + slot )

if not os.path.exists( install_dir ):
  os.makedirs( install_dir )

conda  = os.path.join( install_dir, "bin", "conda" )

if not os.path.exists( conda ):
  print("Installing Miniconda to " + install_dir );
  installer = os.path.join( cwd, "miniconda-installer" )
  os.system( installer + " -b -f -p " + install_dir )

# configure channels"
os.system( conda + " config --add channels omnia" )
os.system( conda + " config --add channels acellera" )

if os.path.exists("dependencies.txt"):
  f = open( "dependencies.txt", "r" )
  lines = f.readlines()
  for dep in lines:
    print("Installing dependency " + dep);
    os.system( conda + " install " + dep + " -y" );

print("Updating distro")
os.system( conda + " update --all -y" )

