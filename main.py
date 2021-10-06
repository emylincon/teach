import time
import paho.mqtt.client as mqtt
from threading import Thread
from matplotlib import pyplot as plt
import os

os.system('clear')
print('-----------------------------------')
print('Welcome to MQTT Subscriber client')
print('-----------------------------------')

username = input('Username of Broker: ').strip()
password = input('Password of Broker: ').strip()
broker_ip = input("Broker's IP: ").strip()
broker_port_no = int(input("Broker's Port no: ").strip())
topic = input("Topic: ").strip()
print('-----------------------------------')

table = [0]
graph_check = 0


def on_connect(connect_client, userdata, flags, rc):
    print("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    connect_client.subscribe(topic)


# Callback Function on Receiving the Subscribed Topic/Message
def on_message(message_client, userdata, msg):
    # print the message received from the subscribed topic
    no = str(msg.payload, 'utf-8')
    if len(table) > 100:
        table.pop(0)
    table.append(int(no))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password)
client.connect(broker_ip, broker_port_no, 60)


def client_loop():
    client.loop_forever()


def handle_close(evt):
    global graph_check
    print('Closed Figure!')
    graph_check = 1


def chat_control():
    global graph_check
    print('--------------------------------------------------')
    print('Hello, Ask me about the temperature')
    print('or maybe you want to see real-time temperature graph')
    print('--------------------------------------------------')
    while True:
        plot_temp_graph()
        plt.show()


def plot_temp_graph():
    fig1 = plt.figure('Temperature Readings in Celsius')

    fig1.canvas.mpl_connect('close_event', handle_close)
    fig1 = plt.clf()
    fig1 = plt.ion()
    # fig1 = plt.grid(True, color='k')
    #fig1 = plt.scatter(table, list(range(0,len(table))), label='Temp C')
    fig1 = plt.plot(table, ':o', label="Current Average = "+str(round(sum(table)/len(table),3)))
    fig1 = plt.title('Telemetry Monitor')
    fig1 = plt.ylabel('Data Value')
    fig1 = plt.xlabel('Time (seconds)')
    fig1 = plt.grid(True)
    fig1 = plt.legend()
    fig1 = plt.pause(1)


def main():
    try:
        h1 = Thread(target=client_loop)
        h1.start()
        time.sleep(2)
        h2 = Thread(target=chat_control)
        h2.start()
    except KeyboardInterrupt:
        print('\nProgramme terminated')


if __name__ == "__main__":
    main()