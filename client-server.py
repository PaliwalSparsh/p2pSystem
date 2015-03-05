import socket
import func
from threading import Thread 
import time
import select
import re
name = raw_input("What is your name? \n")
onlinePeople =[]
def sendo(s): #SENDING MESSAGE
	data = raw_input("")
	while True:
		s.sendall(data)
		data = raw_input("")
		if(data == 'q'):
			
			break
	return
def recvo(s): # RECIEVING MESSAGE
	while True:
		data=s.recv(1024)
		if data:
			print host + ">>"+data
		if data == 'q':
			

			break
	return

def broadcast(s,ip): # BROADCASTING NAME AND IP				
	while 1:
		data = ip +' '+name
		s.sendto(data, ('<broadcast>', 6000))
		time.sleep(2)
def recvBroadcast(s): # RECIEVING IP
	
	while True:
    		result = select.select([s],[],[])
    		msg = result[0][0].recv(1024)
    		if msg:
    			ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', msg ) 
    		if ip[0] not in onlinePeople :
    			onlinePeople.append(ip[0])
    			print ip[0] + ' is online\n'
# CREATING A UDP SOCKET TO SEND
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.bind(('', 0))
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# CREATING A UDP SOCKET TO RECIEVE
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2.bind(('<broadcast>', 6000))
s2.setblocking(0)
host = func.return_ip()
# THREAD TO ALWAYS BROADCAST IP AND ALWAYS SEARCH FOR BROADCASTED IPs
udpThreadSend= Thread(target=broadcast,args=(s1,host,))	
udpThreadRecv= Thread(target=recvBroadcast,args=(s2,))	
#Socket for a tcp connection		
s=socket.socket()

port = 6482
s.bind((host,port))
def tcpServer(s):
	s.listen(1)
	print 'Listening ...'
	while True:
        	 # establish a connection
		clientsocket,addr = s.accept()      
		print("Got a connection from %s" % str(addr))
		try:
			clientsocket.send('Connection Established')
				
			SendS = Thread(target=sendo,args=(clientsocket,))
			RecS  = Thread(target=recvo, args =(clientsocket,))
			SendS.start()
			RecS.start()
			clientsocket.close()
			s.close()
    		
		except:
			print "FUCK\n"
			#clientsocket.close()
def tcpClient(s):
	s= socket.socket()
	host = raw_input("Enter the IP to connect to : ")
	port = 6482
	s.connect((host, port))
	sendCT = Thread(target=sendo,args=(s,))
	recvCT = Thread(target=recvo, args =(s,))
	sendCT.start()
	recvCT.start()
	s.close()
	#s.close()
udpThreadSend.start()
udpThreadRecv.start()
