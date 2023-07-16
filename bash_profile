# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

function optsrc() {
  while [ -n "$1" ]; do
    [ -f "$1" ] && source "$1"
    shift
  done
}

function optpath() {
  while [ -n "$1" ]; do
    [ -d "$1" ] && PATH="$1:$PATH"
    shift
  done
}

HOST=`hostname -s`
EMAIL="matt@hazelmollusk.org"
DEBEMAIL="matt@hazelmollusk.org"
DEBFULLNAME="Matt Barry"
DEBNAME=$DEBFULLNAME

export EMAIL DEBEMAIL DEBFULLNAME DEBNAME
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# PATH changes should go in bashrc
optsrc ~/.bashrc
optsrc ~/.bash_aliases

HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=queSeraSera
shopt -s histappend

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# put a basic xterm title up
printf "\033]0;%s\007" "`whoami`@`hostname -s`"

optsrc $HOME/.asdf/completions/asdf.bash
if ! shopt -oq posix; then
  optsrc /usr/share/bash-completion/bash_completion
  optsrc /etc/bash_completion
  optsrc /opt/homebrew/etc/bash_completion
fi

optsrc ~/.dot/prompt.sh

optsrc ~/.dot/hosts/${HOST}.sh
optsrc ~/.dot/hosts/${HOST}-prompt.sh

optsrc ~/.bash_profile.local

##########
fortune -s
##########
