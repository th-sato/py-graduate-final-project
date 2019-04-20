#!/bin/sh

if [ "$1" = "" ]
then
	echo "Processo iniciado!"
	python web-application/app.py
	echo "Processo finalizado!"
fi
