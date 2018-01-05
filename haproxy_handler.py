#!/usr/bin/env python

import sys
import re
import os
import join
import leave

membership_events = sys.stdin.readlines()
event_array = []

for membership_event in membership_events:
  event_array = membership_event.split('\t')
  event = { 'hostname': event_array[0], 'ipaddress': event_array[1], 'role': event_array[2], 'state': os.environ['SERF_EVENT'] }
  if event['role'] == 'app' and re.match('.*-as-app.*$', event['hostname']):
    if event['state'] == 'member-join':
      join.register(event['ipaddress'])
    elif event['state'] == 'member-leave':
      leave.unregister(event['ipaddress'])
    elif event['state'] == 'member-failed':
      leave.unregister(event['ipaddress'])
