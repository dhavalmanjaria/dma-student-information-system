#!/bin/bash

for x in `find . -name '*.py'`; do cat /home/dhaval/Documents/Python/Django/preamble.py $x | tee $x.bk; cat $x.bk > $x; done 

for x in `find . -name '*.bk'`; do rm $x; done
