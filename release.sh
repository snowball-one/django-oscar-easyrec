#!/bin/bash

parts="patch minor major"

die() {
    echo >&2 "$@"
    exit 1
}

if [ -z "$1" ] || ! [[ "$parts" =~ "$1" ]]
    then
        die "You must specify a version part to bump (patch, minor, major)"
fi

bumpversion $1 
./setup.py sdist upload
git push origin --tags
git push origin master
