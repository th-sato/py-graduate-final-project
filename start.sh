#!/bin/sh

if [ "$1" = "" ]
then
	echo "Processo iniciado!"
	python autonomous_car/start_autonomous_car.py
	echo "Processo finalizado!"
fi
