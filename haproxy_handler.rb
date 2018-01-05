#!/usr/bin/env ruby

membership_events = $stdin.readlines.each do |membership_event|
  event_array = membership_event.split(/\t/)

  event = { :hostname => event_array[0], :ipaddress => event_array[1], :role => event_array[2], :state => ENV['SERF_EVENT'] }

  if event[:role] === 'app' && event[:hostname] =~ /^.*-as-app.*$/ then
    case event[:state]
    when 'member-join'
      %x(/usr/local/bin/register_app_node.py #{event[:ipaddress]})
    when 'member-leave'
      %x(/usr/local/bin/unregister_app_node.py #{event[:ipaddress]})
    when 'member-failed'
      %x(/usr/local/bin/unregister_app_node.py #{event[:ipaddress]})
    end
  end
end
