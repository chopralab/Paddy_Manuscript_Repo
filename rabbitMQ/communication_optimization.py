import pika, sys, os
import optimization


def optimization_send(enzyme_concentration,subtrate_concentration,incubation_time):
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    #this is for sending from optimiziation send to insturment receive 
    channel.queue_declare(queue='instrument_recieve')
    message = 'enzyme_conc {},substrate_conc {},incubation_time {}'.format(enzyme_concentration,subtrate_concentration,incubation_time)
    channel.basic_publish(exchange='', routing_key='instrument_recieve', body=message)
    print(" [x] Sent Optimized Conditions: {} ".format(message))
    connection.close()




def optimizaiton_recieve():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='optimization_recieve')
    #callback function will take aos and run paddy
    channel.basic_consume(queue='optimization_recieve', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        optimization.results_update(float(body.decode()))
        conditions = optimization.bo_run()
        optimization_send(conditions[0],conditions[1],conditions[2])

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