#!/bin/bash
A=$(docker-compose logs | grep -w -c ACCEPT)
B=$(docker-compose logs | grep -w -c CLOSE)
echo "connected:    " $A
echo "disconencted: " $B
echo "current:" $((A-B))
