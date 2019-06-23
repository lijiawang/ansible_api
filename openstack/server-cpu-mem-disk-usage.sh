free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'
df -h -t ext2 -t ext4 | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print "Disk Usage:"" " $1 " " $3"/"$2" ""("$5")"}'
top -bn1 | grep load | awk '{printf "CPU Load: %.2f\n", $(NF-2)}'
