#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)
name=pdf-renderer

pushd "$tmp"
svn checkout https://svn.java.net/svn/pdf-renderer~svn/trunk $name-$date
pushd $name-$date
svn=$(svnversion)svn
find . -type d -name "\.svn" | xargs rm -fr -- || :
popd>/dev/null

# Remove the web content
rm -fr $name-$date/www/

mv $name-$date $name-$svn-$date
tar jcf "$pwd"/$name-$svn-$date.tar.bz2 $name-$svn-$date
echo "Wrote $name-$svn-$date.tar.bz2"
popd >/dev/null
