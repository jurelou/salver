#!/bin/bash
# -*- coding: utf-8 -*-

function test_systems_available {
  COUNTER=0
  until $(curl --output /dev/null --silent --head --fail http://localhost:$1); do
      printf '.'
      sleep 2
      let COUNTER+=1
      if [[ $COUNTER -gt 30 ]]; then
        echo -e '\nWARNING: Could not reach configured kafka system on http://localhost:$1 \nNote: This script requires curl.\n'
        exit 1
      fi
  done
}

test_systems_available 8082
test_systems_available 5601

