#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#this is for sending from optimiziation send to insturment receive 
channel.queue_declare(queue='instrument_recieve')

channel.basic_publish(exchange='', routing_key='instrument_recieve', body='enzyme_conc 0.25,substrate_conc 0.15,incubation_time 25')
print(" [x] Sent 'Hello World!'")

print('i believe this will work')

connection.close()
