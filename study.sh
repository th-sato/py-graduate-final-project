#!/bin/sh

if [ "$1" = "" ]
then
	echo "Iniciado!"
	python autonomous_car/study.py
	echo "Fim!"
fi
