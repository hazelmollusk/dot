APPS=homebrew
[ -d ~/.local/bin ] && export PATH=~/.local/bin:$PATH
[ -d ~/bin ] && export PATH=~/bin:$PATH
for ROOT in /opt /usr/local; do
  for APP in $APPS; do
    [ -d "$ROOT/$APP/bin" ] && export PATH="$ROOT/$APP/bin:$PATH"
  done
done

[ -f "$HOME/.asdf/asdf.sh" ] && source $HOME/.asdf/asdf.sh
