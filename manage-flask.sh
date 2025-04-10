#!/bin/bash

function show_help {
  echo "Usage: $0 [command]"
  echo "Commands:"
  echo "  start        - Deploy the Flask app stack"
  echo "  status       - Check stack status"
  echo "  logs         - Show logs from the Flask app"
  echo "  stop         - Stop the stack"
  echo "  restart      - Restart the stack"
  echo "  update       - Rebuild and update the service"
  echo "  help         - Show this help message"
}

case "$1" in
start)
  ./deploy-flask.sh
  ;;
status)
  echo "Service status:"
  docker stack services flask-app
  echo -e "\nContainer status:"
  docker stack ps flask-app
  ;;
logs)
  docker service logs flask-app_flask-app -f
  ;;
stop)
  docker stack rm flask-app
  echo "Flask app stack stopped"
  ;;
restart)
  docker stack rm flask-app
  echo "Waiting for stack to be removed..."
  sleep 5
  ./deploy-flask.sh
  ;;
update)
  echo "Rebuilding image..."
  docker build -t localhost/flask-websocket-app:latest .
  echo "Updating service..."
  docker service update --force flask-app_flask-app
  ;;
*)
  show_help
  ;;
esac
