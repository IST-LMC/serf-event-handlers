#!/usr/bin/env ruby

membership_event = $stdin.read.split(/\t/)

event = { :hostname => membership_event[0], :ipaddress => membership_event[1], :role => membership_event[2], :state => ENV['SERF_EVENT'] }

if event[:role] === 'app' then
  case event[:state]
  when 'member-join'
    %x(/usr/local/bin/register_app_node.py #{event[:ipaddress]})
  when 'member-leave'
    puts "Drain and remove node from load balancer"
  when 'member-failed'
    puts "Drain and remove node from load balancer"
  end
end
