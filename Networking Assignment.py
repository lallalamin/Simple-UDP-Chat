"""
This is a simple clinet to server chat using UDP

Author: Mari Hirota

Firstly, the program will ask you for hostname or IP
address. Once you type input, the program will run 
server thread and client thread. 

server()
- Receive message from the client
- Implement a simple protocol to send to client that it
  receive the message and print out the message, address,
  and sequence number.
- Will ignore client message sometime

client()
- Ask the user to enter the message they want to send
  to the server
- Send the message to the server and implement a simple
  protocol waiting acknowledgement from the server
- If we encounter timeout, the protocol will resend the 
  message again
- Will ignore server message sometime.

"""

import socket, random, threading

#ask the user for hostname/IP
host_ip = input("Enter the server's hostname or IP address: ")
#define the server address and port
server_address = (f'{host_ip}', 12000)

#reciever  
def server():
    #receiver status variable
    receiver_seq = 0

    #server setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)
    while True:
        data, address = server_socket.recvfrom(2048)
        data = data.decode()
        seq_num_s, message = data[0], data[1:]
        randomNum = random.randint(1,10)
        
        if randomNum < 5: #if server doesnot ignore message
            if int(seq_num_s) == receiver_seq: #if message has correct sequence num
                print("Message from: " + address[0] + " sequence: " + seq_num_s + " message: " + message)
                server_socket.sendto(seq_num_s.encode(), address)
                receiver_seq = 1 - receiver_seq
            else:
                server_socket.sendto(seq_num_s.encode(), address) #ACK Previous message
        else:
            print("server ignored message!")


#sender
def client():
    #sender status variable
    sender_seq = 0

    #create a UDP Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Set time out
    client_socket.settimeout(1.0)

    while True:
        sender_ack_rec = False
        #get message from the user
        message = input("Enter a message to send: ")
        #append a sequence number to said message
        message_to_send = str(sender_seq) + message
        #send the message
        client_socket.sendto(message_to_send.encode(), server_address)

        while not sender_ack_rec: # have not received an ACK
            try:
                #recevive the message
                ack, temp = client_socket.recvfrom(2048)
                #print(ack.decode(), sender_seq)
                ack = ack.decode()
                ack_num = int(ack[0])
                #generate a random num 
                randomNum = random.randint(1, 10)
                if randomNum < 5: #client does not ignore message
                    if sender_seq == ack_num: #has correct sequence number
                        #set ack received = true
                        sender_ack_rec = True
                        sender_seq = 1 - sender_seq  #flip the seq num
                    else:
                        client_socket.sendto(message_to_send.encode(), server_address) #resent the message
                else:
                    print("client ignored ACK!")
            except socket.timeout:
                #on timeout exception, resent the packet 
                client_socket.sendto(message_to_send.encode(), server_address)
            

def run():
    server_thread = threading.Thread(target=server)
    client_thread = threading.Thread(target=client)
    
    server_thread.start()
    client_thread.start()

if __name__ == "__main__":
    run()
