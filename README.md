## Install

`homeshick clone git@github.com:filviu/dot-todotxt.git`

## Dependencies

* Ruby - todo.txt later
* entr - todo.txt watch
* perl, libdatetime-perl, libdatetime-format-duration-perl - recur

## Sources

- todotxt.cli - https://github.com/todotxt/todo.txt-cli

Tool | Usage | URL
-- | -- | --
birdseye | bridseye overview | https://github.com/karbassi/todotxt-birdseye.git
due | manipulate due dates | https://github.com/mdzimmerman/todo.txt-cli-due
later | later recuring tasks | https://github.com/opennomad/todo.txt-later
recur | recuring task tracking done | https://github.com/silviuvulcan/todo.txt-recurring-tasks
todosh_plugins | recur and agenda not really used | https://github.com/sercxanto/todosh_plugins
watch | live watch | https://github.com/munkee/todo.txt-watch


## process-later-dues.sh

Script that replaces due:today, due:tomorrow or due:NNth / 1st with 
the proper formated date allowing later to have working due dates.

Obviously only works if ran the same day as todo.sh later. Easy to run 
from the same cron entry, as below.

Also if you run later the same day you get the task again (because
the tomorrow/NNth is different than the already replaced date)

## Cron

```
# todo.txt
   0 6 * * * ~/bin/todo.sh recur >/dev/null 2>&1
  10 6 * * * ~/bin/todo.sh later >/dev/null 2>&1 ; ~/bin/process-later-dues.sh >/dev/null 2>&1
```
