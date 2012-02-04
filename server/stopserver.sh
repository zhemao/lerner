#!/bin/sh

case $1 in
	web)
		PIDFILE="~/.lerner/webserver.pid"
		if [ -f $PIDFILE ]; then
			kill `cat $PIDFILE`
		fi ;;
	pubsub)
		PIDFILE="~/lerner/pubsubserver.pid"
		if [ -f $PIDFILE ]; then
			kill `cat $PIDFILE`
		fi ;;
	*)
		$0 web
		$0 pubsub ;;
esac
