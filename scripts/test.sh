#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
while getopts ":s" arg; do
	case $arg in
	s)
		find "$SCRIPT_DIR"/../build -type f -iname '*.ttf' -print0 | xargs -I{} "$SCRIPT_DIR"/../src/stat.py {}
		;;
	*) ;;
	esac
done

cat "$SCRIPT_DIR"/../test/pattern.txt
