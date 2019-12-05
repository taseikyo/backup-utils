#!/bin/bash
# @Date    : 2019-11-07 9:32:10
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo

# print cpu information (l1 - l3 cache size/type)

unshared () {
    grep '^[0-9]\+$' "$1" > /dev/null
}

for cpu in $(ls -d /sys/devices/system/cpu/cpu[0-9]* | sort -t u -k 3 -n); do
    echo "${cpu##*/}: [Package #$(cat $cpu/topology/physical_package_id), Core #$(cat $cpu/topology/core_id)]"
    if ! unshared $cpu/topology/core_siblings_list; then
        echo "  same package as $(cat $cpu/topology/core_siblings_list)"
    fi
    if ! unshared $cpu/topology/thread_siblings_list; then
        echo "  same core as    $(cat $cpu/topology/thread_siblings_list)"
    fi
    for cache in $cpu/cache/index*; do
        printf "  %-15s " "L$(cat $cache/level) $(cat $cache/type):"
        echo "$(cat $cache/size) $(cat $cache/ways_of_associativity)-way with $(cat $cache/coherency_line_size) byte lines"
        if ! unshared $cache/shared_cpu_list; then
            printf "  %-15s [%s]\n" "" "shared with $(cat $cache/shared_cpu_list)"
        fi
    done
    echo
done