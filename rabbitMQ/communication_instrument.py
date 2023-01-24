#Communication module for instrument to talk to rabbitMQ

import math
import numpy as np
import pika, sys, os
# from instrument import assay_optimization_score
import instrument
import time


#Send Assay_optimization_score to optimization_recieve based on the parameters that were run on the instrument
def instrument_send(aos):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    #this is for sending from instrument send to optimization receive 
    channel.queue_declare(queue='optimization_recieve')
    channel.basic_publish(exchange='', routing_key='optimization_recieve', body=str(aos))
    print('Instrument experiment complete.')
    time.sleep(2)
    print("|Result| Results of experiment = %r" % str(aos))
    time.sleep(3)
    print("[x] Sending results to optimizer. \n" )
    print('-------------------------------------------')
    print('------------------------------------------- \n')
    time.sleep(2)
    connection.close()

#Recieve optimized parameters to run on the instrument from optimization_send
def instrument_recieve():
    time.sleep(5)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    #this is for sending from optimiziation send to insturment receive 
    channel.queue_declare(queue='instrument_recieve')
    channel.basic_consume(queue='instrument_recieve', on_message_callback=callback, auto_ack=True)

    print('|Schedule| [*] Instrument is waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

#What happens when instrument_recieve is pinged
def callback(ch, method, properties, body):
    time.sleep(3)
    print("[x] Instrument received optimized parameters from the optimizer.")
    time.sleep(2)
    print("|Command| Initating new run on instrument with parameters: \n %r" % body.decode())
    # message should be in form enzyme_conc x,substrate_conc y,incubation_time t
    enzyme_conc = float(body.decode().split(',')[0].split(' ')[1])
    substrate_conc = float(body.decode().split(',')[1].split(' ')[1])
    incubation_time = float(body.decode().split(',')[2].split(' ')[1])
    aos = instrument.assay_optimization_score(enzyme_conc, substrate_conc, incubation_time)
    instrument_send(aos)

def main():
    instrument_recieve()

if __name__=='__main__':
    main()