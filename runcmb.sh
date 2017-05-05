#!/bin/bash

echo Using $(which python3.6)

while true
do
	python3.6 .
	echo "Bot died, restarting in 3s..."
	sleep 3
done