source ~/.dot/colors.sh

DIRCOLOR=$BLACK$BG2w
PIPECOLOR="$NORMAL\[\033[02;${PCOLOR}m\]"
HOSTCOLOR="\[\033[${HCOLOR}m\]"
HOSTCOLORDIM="\[\033[02;${HCOLOR}m\]"
SWISH="█▓▒░"

SPACE='  '
SPACE2='    '
function prompt_pre() {
  unset GIT
  declare -A GIT
  GIT_STATUS=`git status -b --porcelain=1 2>&1`
  if [[ ! $GIT_STATUS =~ fatal ]]; then
      GIT[NAME]=`git config --get remote.origin.url | sed -e 's/^.*\/\([^/.]*\).*/\1/' 2>&1`
      GIT[BRANCH]=`git branch --show-current 2>&1`
      if [[ $GIT_STATUS =~ behind ]]; then
        GIT[BEHIND]="»"
      fi
      if [[ $GIT_STATUS =~ ahead ]]; then
        GIT[AHEAD]="«"
      fi
      if [[ $GIT_STATUS =~ ^\?\? ]]; then
        GIT[UNTRACKED]="?"
      fi
      if [[ $GIT_STATUS =~ ^\ M ]]; then
        GIT[MODIFIED]="¤"
      fi
  fi
  DDATE=`ddate +%A 2>/dev/null || date +%A 2>/dev/null`
  TIME=`date +%I%M`
  DISPLAY_PATH=$(p="${PWD#${HOME}}"; [ "${PWD}" != "${p}" ] && printf "~";IFS=/; for q in ${p:1}; do printf /${q:0:1}; done; printf "${q:1}")
  PS1="\033]0;$USER@$HOST: ${DISPLAY_PATH} | ${GIT[ORIGIN]} ${GIT[BRANCH]:+(${GIT[BRANCH]})} ${GIT[UNTRACKED]:+\?}${GIT[MODIFIED]:+*}\007\
$NORMAL$DIM${CYAN}▄\
$BOLD$WHITE$BLUEBG\
$SPACE2$DDATE${SPACE}$DIM${CYAN}│$SPACE$NORMAL$WHITE$BLUEBG$TIME$SPACE2\
${NORMAL}${LIGHT}${CYAN}${BLUEBG}▒░\
${debian_chroot:+($debian_chroot) }\
${VIRTUAL_ENV:+($(basename $VIRTUAL_ENV)) }\
${CYAN}${BLUEBG}\
$SPACE\u\
${BLUE}${CYANBG}\
\h$SPACE\
${NORMAL}${CYAN}▒░\
$NORMAL$SPACE${GIT[NAME]}$BOLD$DIM$CYAN ■ $NORMAL$BOLD$WHITE${GIT[BRANCH]}\
$SPACE\
$BOLD$YELLOW${GIT[MODIFIED]}\
$BOLD$RED${GIT[UNTRACKED]}\
$BOLD$DIM$BLUE${GIT[BEHIND]}\
$BOLD$DIM$GREEN${GIT[AHEAD]}\

$NORMAL$DIM${CYAN}▀$NORMAL ${DISPLAY_PATH} \
$NORMAL$BOLD\$$NORMAL "

  cols=$(tput cols)
  if [[ -v simple || $cols -lt 60 ]]; then
  PS1="\
${VIRTUAL_ENV:+$FG4($WHITE$(basename $VIRTUAL_ENV)$FG4) }\
$GREEN\u\
$PURPLE@\
$GREEN\h:\
$BOLD$BLUE $DISPLAY_PATH \
$NORMAL$WHITE\$ \
"
  fi
}

PROMPT_COMMAND='prompt_pre'
trap 'printf "\033]0;%s\007" "${BASH_COMMAND//[^[:print:]]/}"' DEBUG
