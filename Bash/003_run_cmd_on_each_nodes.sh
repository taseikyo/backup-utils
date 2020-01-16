#!/bin/bash
# @Date    : 2020-01-10 9:32:10
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo

# run input command on each node

[[ ! "$#" -ge 1 ]] && echo "do you input the command?" && exit 1

nr_nodes=`numactl -H | grep -oP "\d+\)" | grep -oP "\d"`

echo "we have $nr_nodes numa nodes."
for i in $(seq 0 $nr_nodes); do
    echo -e "\nnode $i:"
    numactl --membind=$i $1
done