X=`realpath "${BASH_SOURCE[0]}"` X=`dirname "$X"` X=`realpath "$X/../.."` DOT_ROOT=$X
export DOT_ROOT
export DOT_HOST=`hostname -s`
export DOT_USER=`whoami`

function optsrc() {
  while [ -n "$1" ]; do
  #echo -n "INCLUDING $1... "
    [ -f "$1" ] && source "$1" #&& echo '$' || echo '!'
    shift
  done
}

function optpath() {
  while [ -n "$1" ]; do
    [ -d "$1" ] && PATH="$1:$PATH"
    shift
  done
}
