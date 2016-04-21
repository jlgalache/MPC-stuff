#!/bin/csh -f

cd /base/public

# export PYTHONPATH=/home/mpc/mpcops/lib
set PYTHONPATH=/home/mpc/mpcops/lib

if $# == 0 then
  set filename = 'MPCORB.DAT'
else
  set filename = $1
endif

python3 make_mpcorb_extended.py $filename


end