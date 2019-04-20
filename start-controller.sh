#!/bin/sh

if [ "$1" = "" ]
then
	echo "Processo iniciado!"
	python autonomous_car/app.py
	echo "Processo finalizado!"
fi
