#!/bin/bash

export CACHE_DIR="./cache"

while true; do
    read document
    export DOC_FNAME="document.xml"
    export DOC_FDIR=$CACHE_DIR/"$(basename "$DOC_FNAME").dir"

    export DOC_FDIR_TEXT="$DOC_FDIR"/"doc.txt"
    export DOC_FDIR_LINKS="$DOC_FDIR"/"links.json"

    echo $DOC_FDIR
    python3 __main__.py
    cat "$DOC_FDIR_TEXT"
    read cmd
    if [[ $cmd = "X" ]];then
        break
    fi
done