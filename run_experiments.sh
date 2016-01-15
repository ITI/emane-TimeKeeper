#!/bin/bash

N_iterations=1
TDF_COUNTER=5
TDF_STEP_SIZE=2
MAX_TDF=11
i=0
while [ $i -lt $N_iterations ]; do
	while [ $TDF_COUNTER -lt $MAX_TDF ]; do
        	echo The current TDF is $TDF_COUNTER
		cd tests/large_linear 
		sudo python large_linear.py $TDF_COUNTER
		cd ../../; 
		sudo python deploy.py $(pwd)/tests/large_linear
		let TDF_COUNTER=TDF_COUNTER+TDF_STEP_SIZE
	done
	let i=i+1
done

