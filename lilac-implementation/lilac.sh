#!/bin/bash

print_usage() {
  printf "usage: lilac [-options] [path to file]\n\t-v | Verbose: Print debug info"
}

lilac(){
  debug_level='INFO'
  
  if [[ $# == 1 ]]; then
    python main.py
  elif [[ $# > 1 ]]; then
    while getopts 'diwe:' flag; do
      case "${flag}" in
        d) debug_level='DEBUG' ;;
        i) debug_level='INFO' ;;
        w) debug_level='WARN' ;;
        e) debug_level='ERROR' ;;
        *) print_usage ;;
      esac
    done
    python main.py $1 "$debug_level"
  fi
}
