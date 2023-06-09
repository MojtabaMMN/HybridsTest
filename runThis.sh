#!/bin/bash

myName=$0
myDir=`dirname ${myName}`
cd ${myDir}

rm output/*

targetDir=/eos/project/c/cmsweb/www/tracker-upgrade/hybridProduction/output
./cumulativePlot.py

if [ -d ${targetDir} ] ; then
	cp output/* "${targetDir}"
fi
