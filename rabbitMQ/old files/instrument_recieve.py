import math
import numpy as np
import pika, sys, os
from instrument_send import send_optimization_score

def assay_optimization_score(enzyme_conc, substrate_conc, incubation_time):
    aos = 10000*min(max(0.52-0.495,0),0.025)/((25*enzyme_conc) + (5*substrate_conc) + (incubation_time))
    #z < 0.52 undesirable
    return aos

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    #this is for sending from optimiziation send to insturment receive 
    channel.queue_declare(queue='instrument_recieve')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        #message should be in form enzyme_conc x,substrate_conc y,incubation_time t
        enzyme_conc = float(body.decode().split(',')[0].split(' ')[1])
        substrate_conc = float(body.decode().split(',')[1].split(' ')[1])
        incubation_time = float(body.decode().split(',')[2].split(' ')[1])
        print(assay_optimization_score(enzyme_conc, substrate_conc, incubation_time))
        aos = assay_optimization_score(enzyme_conc, substrate_conc, incubation_time)
        send_optimization_score(aos)

    channel.basic_consume(queue='instrument_recieve', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)



assay_optimization_score(0.55,0.33,25)

