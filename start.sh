#!/bin/sh
if [ "$1" = "" ]
then
	echo "Processo iniciado!"
	python start_system.py
	echo "Processo finalizado!"
fi
