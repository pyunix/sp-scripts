#!/bin/sh
# -------------------------------------------------------------------------
# Remove the stuff we don't want

unset PROMPT_COMMAND
unset LS_COLORS

ALIASES=$(alias |cut -f2 -d' '|cut -f1 -d'=')
for i in $ALIASES
do
    unalias $i >/dev/null 2>&1
done
unset ALIASES
unset i

complete -r

DECS="$(declare -F |awk '{print $3}')"
for i in $DECS
do
    unset $i
done
unset DECS
unset i

# Build a list of all envs, exclude the ones BASH likes to keep.
#ENVS="$(declare -p |awk '{print $3}' |cut -f1 -d'='|egrep -v \
#    '^BASHOPTS$|^BASHPID$|^BASH_ARGC$|^BASH_ARGV$|^BASH_LINENO$|^BASH_REMATCH$|^BASH_SOURCE$|^BASH_VERSINFO$|^EUID$|^PPID$|^SHELLOPTS$|^TMOUT$|^UID$' \
#    )"

ENVS="$(set |cut -f1 -d'=')"

for i in $ENVS
do
    case "$i" in
        "BASHOPTS" ) ;;
        "BASHPID" ) ;;
        "BASH_ARGC" ) ;;
        "BASH_ARGV" ) ;;
        "BASH_LINENO" ) ;;
        "BASH_REMATCH" ) ;;
        "BASH_SOURCE" ) ;;
        "BASH_VERSINFO" ) ;;
        "EUID" ) ;;
        "PPID" ) ;;
        "SHELLOPTS" ) ;;
        "TMOUT" ) ;;
        "UID" ) ;;
        *) unset $i
    esac
done
unset ENVS
unset i

# We'll need this one shortly...
export PATH=/sbin:/bin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

# -------------------------------------------------------------------------
# Add the stuff we do want

[ "$(alias a > /dev/null 2>&1)" ] || alias a='ssh-add ~/.ssh/id_ed25519'
[ "$(alias g > /dev/null 2>&1)" ] || alias g='ssh-add ~/.ssh/id_ed25519_sap'
[ "$(alias c > /dev/null 2>&1)" ] || alias c='clear'
[ "$(alias l > /dev/null 2>&1)" ] || alias l='ssh-add -l'
[ "$(alias s > /dev/null 2>&1)" ] || alias s='eval $(ssh-agent -s)'
[ "$(alias sp > /dev/null 2>&1)" ] || alias sp='. ~/.sp'
[ "$(alias x > /dev/null 2>&1)" ] || alias x='[$SSH_AGENT_PID] && kill $SSH_AGENT_PID ; exit'

k() {
    i=$(ps -u $LOGNAME |grep ssh-agent |awk '{print $1}')
    [ -z "$i" ] && printf "No SSH Agents Running\n" || kill $i
}
unset i



# Server specific settings
set -o vi
umask 077

# Good stuff from /etc/bashrc
shopt -s histappend
history -a
shopt -s checkwinsize

# Now figure out who we really are and set up useful vars.

export LOGNAME="$(id -un)"
export HOME="$(getent passwd $LOGNAME |cut -f6 -d':')"
if [ ! -d "$HOME" ]
then
    printf "Trying to set up a HOME directory: /tmp/$LOGNAME\n"
    mkdir -p "/tmp/$LOGNAME" && export HOME="/tmp/$LOGNAME"
fi

cd "$HOME"

export BASH=/bin/bash
export BASHRCSOURCED=Y
export HISTCONTROL=ignoredups
export HISTFILE="$HOME/.bash_history"
export HISTFILESIZE=1000
export HISTSIZE=1000
export HOSTNAME="$(uname -n)"
export IFS=$' \t\n'
export KRB5CCNAME=KCM:
export LANG=en_NZ.UTF-8
export PS2='> '
export PS4='+ '
export SHELL=/bin/bash
export TERM=xterm

for i in ~/.spcolors
do
    if [ -f "$i" ] ; then
        printf "Running $i\n"
        . "$i"
    fi
done
printf "$SPCOLOR"
export PS1="\033]0;\u@\h:\w\007${SPCOLOR}\u@\H:\w\n\\$ "
#       PROMPT_COMMAND='printf "\033]0;%s@%s:%s\007" "${USER}" "${HOSTNAME%%.*}" "${PWD/#$HOME/\~}"'
unset i

