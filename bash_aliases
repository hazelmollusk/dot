alias python=python3

alias bu=vi
alias bi=vi
alias got=git
alias gut=git
alias yawn=yarn

alias hgrep="history|grep"
alias vpn='sudo openvpn /etc/openvpn/us802.nordvpn.com.tcp443.ovpn '
alias dys='ssh dysnomia.cyberdiscordia.org'
alias be='bundle exec'
alias ov='pushd ~/hack/overseer'
alias oc='pushd ~/hack/orbital_command'
alias tssh="tsh ssh -l ec2-user $*"

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
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

alias gc="git commit -am '$*'"
alias ga="git add $*"
alias gl="git list $*"
alias gd="git diff $*"
alias gu="git pull"
alias gcp="git commit -am '$*' && git push"
