
CMD_FNAME="stacked_commands.txt"

CMDS="commands/large-public-subsets/$CMD_FNAME"

function getline { echo $(sed "$1 q;d" $CMDS); }

for i in {1..70}; do
  eval $(getline $i)
done
