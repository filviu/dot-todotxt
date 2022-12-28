#!/bin/bash
todo_file="$HOME/Nextcloud/notes/todo.txt"

today=`date +%Y-%m-%d`
tomorrow=`date +%Y-%m-%d -d "tomorrow"`
current_YM=`date "+%Y-%m"`

sed -i "s/due:tomorrow/due:$tomorrow/g;             \
        s/due:today/due:$today/g;                   \
        s/due:\([0-9]*\)\(th\|st\)/due:$current_YM-\1/g     \
    " $todo_file
