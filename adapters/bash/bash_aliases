# preference/version-lock
which python3  >/dev/null  && alias python=python3

# speling
which vi >/dev/null        && alias bu=vi && alias bi=vi
which git >/dev/null       && alias got=git && alias gut=git
which yarn >/dev/null      && alias yawn=yarn

# shortcut
alias hgrep="history|grep"
alias be='bundle exec'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# color
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'
    alias diff='diff --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
    alias ip='ip -color=auto'
fi

# git
alias gc="git commit -am '$*'"
alias ga="git add $*"
alias gl="git list $*"
alias gd="git diff $*"
alias gu="git pull"
alias gcp="git commit -am '$*' && git push"

# debian
alias up="sudo apt update && sudo apt full-upgrade -y"
