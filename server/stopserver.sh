#!/bin/sh

case $1 in
	web)
		PIDFILE="$HOME/.lerner/webserver.pid"
		if [ -f $PIDFILE ]; then
			kill `cat $PIDFILE`
			rm $PIDFILE
		fi ;;
	pubsub)
		PIDFILE="$HOME/.lerner/pubsubserver.pid"
		if [ -f $PIDFILE ]; then
			kill `cat $PIDFILE`
			rm $PIDFILE
		fi ;;
	*)
		$0 web
		$0 pubsub ;;
esac
