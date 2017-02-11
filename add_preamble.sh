#!/bin/bash


for x in `find . -name '*.py'`; do
        if [[ $(cat $x | grep 'gnu.org') ]]; then
            continue
        fi
        cat /home/dhaval/Documents/Python/Django/preamble.py $x | tee $x.bk
        cat $x.bk > $x    
    done 

for x in `find . -name '*.bk'`; do rm $x; done
