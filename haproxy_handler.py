#!/usr/bin/env python

import sys
import re
import os
import join
import leave

membership_events = sys.stdin.readlines()
event_array = []

for membership_event in membership_events:
  if os.environ['SERF_EVENT'] == 'user':
    event_array = membership_event.split(':')
  else:
    event_array = membership_event.split('\t')

  event = { 'hostname': event_array[0], 'ipaddress': event_array[1], 'role': event_array[2], 'state': os.environ['SERF_EVENT'] }
  try:
    event['hookname'] = event_array[3]
    event['groupname'] = event_array[4]
    event['actiontoken'] = event_array[5]
    event['instance_id'] = event_array[6]
  except:
    print("No Lifecycle Hook Info")

  if event['role'] == 'app' and re.match('.*-as-app.*$', event['hostname']):
    if event['state'] == 'member-join':
      join.register(event['ipaddress'])
    elif event['state'] == 'member-leave':
      leave.unregister(event['ipaddress'])
    elif event['state'] == 'member-failed':
      leave.unregister(event['ipaddress'])
    elif event['state'] == 'member-reap':
      print("% reaped." % event['hostname'])
  elif os.environ['SERF_USER_EVENT'] == 'drain':
    leave.drain(event)
