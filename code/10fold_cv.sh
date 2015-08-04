#!/usr/bin/env bash
# assuming gpu. change the 1's if needbe
if [ $# -lt 2 ]
  then
    echo "Proper usage: sh 10fold_cv.sh <dataset> <algorithm>"
    echo "Example: sh 10fold_cv.sh diabetes SdA.py"
    exit
fi

res_loc1="../results/"
res_loc2=$2
res_loc3="_gpu/fold0"
res_loc=$res_loc1$res_loc2$res_loc3
out=".out"

for i in `seq 1 10`;
do
    python pickle_data.py $1 $i
    if [ $i -lt 10 ]
    then
        res=$res_loc$i$out
        python $2 1 $1 $i >> $res
    else
        python $2 1 $1 $i >> "../results/fold10.out"
    fi
done