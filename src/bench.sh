#!/bin/sh

export ITERATIONS=100
if [ "x$1" == "xfull" ]; then
    export ITERATIONS=10000
fi

cd $(dirname $0)

echo Iterations: $ITERATIONS

printf '' > outfile

django/bench.sh | tee -a outfile
peewee/bench.sh | tee -a outfile
pony/bench.sh | tee -a outfile
sqlalchemy/bench.sh | tee -a outfile
sqlobject/bench.sh | tee -a outfile
CONCURRENTS=1 tortoise/bench.sh | tee -a outfile
CONCURRENTS=10 tortoise/bench.sh | tee -a outfile

cat outfile | ./present.py

rm -f outfile
