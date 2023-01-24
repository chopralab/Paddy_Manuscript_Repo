#Communication module for optimizer to talk to rabbitMQ

#Pika is used for rabbitMQ
import pika, sys, os
import optimization
import time

#Send optimized parameters to instrument
def optimization_send(enzyme_concentration,subtrate_concentration,incubation_time):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    #this is for sending from optimiziation send to insturment receive 
    channel.queue_declare(queue='instrument_recieve')
    message = 'enzyme_concentration: {},substrate_concentration: {},incubation_time: {}'.format(enzyme_concentration,subtrate_concentration,incubation_time)
    channel.basic_publish(exchange='', routing_key='instrument_recieve', body=message)
    # print(" Optimizer has optimized conditions for instrument and selected parameters: \n{} ".format(message))
    time.sleep(3)
    print("|Command| [x] Sent optimized conditions to instrument \n")
    print('-------------------------------------------')
    print('-------------------------------------------')
    time.sleep(2)
    connection.close()



#Recieve Assay score from the instrument based on the parameters that were run
def optimizaiton_recieve():
    time.sleep(3)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='optimization_recieve')
    #callback function will take aos and run paddy
    channel.basic_consume(queue='optimization_recieve', on_message_callback=callback, auto_ack=True)

    print('|Schedule| [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

#What happens when optimization_recieve is pinged
def callback(ch, method, properties, body):
        time.sleep(7)
        print("[x] Received results from instrument experiment")
        time.sleep(2)
        print("|Result| Instrument experiment results score: \n %r" % body.decode())
        time.sleep(2)
        print('|Command| Initiating optimizer to select new conditions')
        time.sleep(2)
        optimization.results_update(float(body.decode()))
        conditions = optimization.bo_run()
        optimization_send(conditions[0],conditions[1],conditions[2])

#Initialize optimization if no loop exists 
def main():
    optimization.initialize_optimization()
    conditions = optimization.bo_run()
    optimization_send(conditions[0],conditions[1],conditions[2])
    optimizaiton_recieve()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)