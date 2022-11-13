cd /Users/meizhenchen/Desktop/Project/oiclass-answers/ || exit
git add .
# shellcheck disable=SC2209
date_time=$(date)
# shellcheck disable=SC2154
git commit -m "Update in $date_time"
git push -u origin main
