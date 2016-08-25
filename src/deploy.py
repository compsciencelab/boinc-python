#!/usr/bin/env python2

from __future__ import print_function

import os
import re
import zipfile
import glob

# Get slot dir
cwd = os.getcwd()

slot = "0"
if re.match( "^.*/slot-[0-9]*$", cwd ):
  slot = re.sub( "^.*/slot-", "", cwd );

home =os.path.expanduser("~")
install_dir = os.path.join( home, ".gpugrid", "slot-" + slot )

if not os.path.exists( install_dir ):
  os.makedirs( install_dir )

conda   = os.path.join( install_dir, "bin", "conda" )
python  = os.path.join( install_dir, "bin", "python" )

if not os.path.exists( conda ) or not os.path.exists(python):
  print("Installing Miniconda to " + install_dir );
  installer = os.path.join( cwd, "miniconda-installer" )
  os.system( installer + " -b -f -p " + install_dir )
# TODO:
# pre-emptively remove any conda lock files
# eg /home/x/.gpugrid/slot-0/pkgs/.conda_lock-21591

# configure channels"
os.system( conda + " config --add channels omnia" )
os.system( conda + " config --add channels acellera" )

if os.path.exists("dependencies.txt"):
  f = open( "dependencies.txt", "r" )
  lines = f.readlines()
  for dep in lines:
    dep = dep.strip()
    print("Installing dependency " + dep);
    os.system( conda + " install " + dep + " -y" );

print("Updating distro")
os.system( conda + " update --all -y" )

if os.path.exists("input.zip"):
  print("Extracting payload data")
  os.path.mkdir( "input" )
  zf=zipfile.ZipFile( "input.zip" )
  zf.extractall( "input" )
  zf.close()

if os.path.exists("payload.py"):
  print("Running payload")
  os.system( python + " payload.py" )

if os.path.exists("output"):
  print("Creating output archive");
  zf = zipfile.ZipFile("output.zip", "w" )
  for f in os.listdir("output"):
    print("  Adding " + f );
    zf.write( os.path.join("output", f), arcname=f )
  zf.close()
