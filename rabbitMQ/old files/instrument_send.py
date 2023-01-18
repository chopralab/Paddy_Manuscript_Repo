#!/usr/bin/env python
import pika


def send_optimization_score(aos):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    #this is for sending from instrument send to optimization receive 
    channel.queue_declare(queue='optimization_recieve')
    channel.basic_publish(exchange='', routing_key='optimization_recieve', body=str(aos))
    connection.close()
    


