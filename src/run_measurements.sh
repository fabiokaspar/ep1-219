#! /bin/bash

set -o xtrace

#ITERATIONS_SIZE=10


ITERATIONS_SIZE=4
INITIAL_SIZE=16

NTHREADS_MAX=32
MEASUREMENTS=10

SIZE=$INITIAL_SIZE

NAMES=('mandelbrot_seq' 'mandelbrot_pth' 'mandelbrot_omp')
MODOS=('com' 'sem')


make
mkdir results
mkdir graphics

for NAME in ${NAMES[@]}; do
    mkdir results/$NAME
    mkdir graphics/$NAME


    if [ $NAME = 'mandelbrot_seq' ] 
    then    
        for MODO in ${MODOS[@]}; do 
            for ((i = 1; i <= $ITERATIONS_SIZE; i++)); do
                for ((j = 1; j <= MEASUREMENTS; j++)); do

                    perf stat -r 1 ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $MODO >> "full_$MODO.log" 2>&1
                    perf stat -r 1 ./$NAME -0.8 -0.7 0.05 0.15 $SIZE $MODO >> "seahorse_$MODO.log" 2>&1
                    perf stat -r 1 ./$NAME 0.175 0.375 -0.1 0.1 $SIZE $MODO >> "elephant_$MODO.log" 2>&1
                    perf stat -r 1 ./$NAME -0.188 -0.012 0.554 0.754 $SIZE $MODO >> "triple_spiral_$MODO.log" 2>&1
                done
                
                SIZE=$(($SIZE * 2))
            done

            SIZE=$INITIAL_SIZE
            mv *.log results/$NAME
       done

    else
        MODO=${MODOS[0]}  #mude para 1 para NÃO obter a I/O
            for ((NT = 1; $NT <= $NTHREADS_MAX; NT = $(($NT * 2)) )); do

                for ((i = 1; i <= $ITERATIONS_SIZE; i++)); do
                    for ((j = 1; j <= MEASUREMENTS; j++)); do

                        perf stat -r 1 ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $NT $MODO >> 'full_'$NT'.log' 2>&1
                        perf stat -r 1 ./$NAME -0.8 -0.7 0.05 0.15 $SIZE $NT $MODO >> 'seahorse_'$NT'.log' 2>&1
                        perf stat -r 1 ./$NAME 0.175 0.375 -0.1 0.1 $SIZE $NT $MODO >> 'elephant_'$NT'.log' 2>&1
                        perf stat -r 1 ./$NAME -0.188 -0.012 0.554 0.754 $SIZE $NT $MODO >> 'triple_spiral_'$NT'.log' 2>&1
                    done
                    
                    SIZE=$(($SIZE * 2))

                done

                SIZE=$INITIAL_SIZE
                mv *.log results/$NAME
            done
    fi

done

#rm *.ppm




