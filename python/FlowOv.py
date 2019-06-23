import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675
import json
import socket
import signal
import thread
import time

PROFILES = '../html/profiles/profiles.json'
FREQUENCY =  1 #Hz
SPI_PORT   = 0
SPI_DEVICE = 0

def load_profiles() :
    f = open(PROFILES,'r')
    p = json.load(f)
    f.close()

    return p

def make_csv(fname, time, temp) :
    out = ""

    for i in range(len(time)) :
        out += "%s,%s\n"%(str(time[i]),str(temp[i]))    

    f = open(fname,'w')
    f.write(out)
    f.close()

def build_tempProfile(profile, frequency = 1) :
    times = profile['time']
    tempC = profile['tempC']

    num_points = len(times)
    idx = 0

    otime = []
    otemp = []

    while idx < (num_points-1) :
        y1 = tempC[idx]
        y2 = tempC[idx + 1]
        x1 = times[idx]
        x2 = times[idx + 1]

        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        t = x1 
        while t < x2 :
            otime.append(t)
            otemp.append(m*t+b)
            t += 1 / frequency
        idx += 1

    return otime, otemp

def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

def RunProfile(profile) :
    sensor = MAX6675.MAX6675(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    times,temps = build_tempProfile(profile,FREQUENCY)

    for target in temps :
        temp = sensor.readTempC()
        print 'Thermocouple Temperature: %s°C'%temp

        if temp < target :
            # Turn On Heating Elements

        else :
            # Turn Off Heating Elements

        time.sleep(1/FREQUENCY)


class Server:
 """ Class describing a simple HTTP server objects."""

 def __init__(self, port = 81):
     """ Constructor """
     self.host = ''   # <-- works on all avaivable network interfaces
     self.port = port 
     self.www_dir = 'www' # Directory where webpage files are stored
    
  
 def activate_server(self):
     """ Attempts to aquire the socket and launch the server """ 
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     try: # user provided in the __init__() port may be unavaivable
         print("Launching HTTP server on ", self.host, ":",self.port)
         self.socket.bind((self.host, self.port)) 
         
     except Exception as e:
         print ("Warning: Could not aquite port:",self.port,"\n")
         print ("I will try a higher port")
         # store to user provideed port locally for later (in case 8181 fails)
         user_port = self.port 
         self.port = 8181
         
         try:
             print("Launching HTTP server on ", self.host, ":",self.port)
             self.socket.bind((self.host, self.port))
             
         except Exception as e:
             print("ERROR: Failed to acquire sockets for ports ", user_port, " and 8181. ")
             print("Try running the Server in a privileged user mode.")
             self.shutdown()
             import sys
             sys.exit(1)
            
     print ("Server successfully acquired the socket with port:", self.port)
     print ("Press Ctrl+C to shut down the server and exit.")
     self._wait_for_connections()
  
 def shutdown(self):   
     """ Shut down the server """
     try:
         print("Shutting down the server")
         s.socket.shutdown(socket.SHUT_RDWR)
         
     except Exception as e:
         print("Warning: could not shut down the socket. Maybe it was already closed?",e)
  
     
 def _gen_headers(self,  code):
     """ Generates HTTP response Headers. Ommits the first line! """
     
     # determine response code
     h = ''
     if (code == 200):
        h = 'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\n'
     elif(code == 404):
        h = 'HTTP/1.1 404 Not Found\n'
     
     # write further headers
     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) 
     h += 'Date: ' + current_date +'\n'
     h += 'Server: Simple-Python-HTTP-Server\n'
     h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request

     return h

 def _wait_for_connections(self):

     global profiles
     
     """ Main loop awaiting connections """
     while True:
         print ("Awaiting New connection")
         self.socket.listen(3) # maximum number of queued connections
         
         conn, addr = self.socket.accept()
         # conn - socket to client
         # addr - clients address
         
         print("Got connection from:", addr)
         
         data = conn.recv(1024) #receive data from client
         string = bytes.decode(data) #decode it to string
         
         #determine request method  (HEAD and GET are supported)
         request_method = string.split(' ')[0]
         print ("Method: ", request_method)
         print ("Request body: ", string)
         
         #if string[0:3] == 'GET':
         if (request_method == 'GET') | (request_method == 'HEAD'):
             #file_requested = string[4:]

             # split on space "GET /file.html" -into-> ('GET','file.html',...)
             file_requested = string.split(' ')
             file_requested = file_requested[1] # get 2nd element
    
             #Check for URL arguments. Disregard them
             file_requested = file_requested.split('?')[0]  # disregard anything after '?'
     
             file_requested = file_requested.split('/')
             response_content = ""
             
             if (file_requested[1] == ''):  # in case no file is specified by the browser
                file_requested = 'none' # load index.html by default
                response_content = "FlowOv - No Command"
             elif ('Run' in file_requested[1]):
                 try :

                     #t = file_requested[1].split('@')[1]
                     #set_temps(serialHandler,t)
                     response_content = "Running Profile %s"%file_requested[2]
                     thread.start_new_thread(RunProfile,(profiles[file_requested[2]],))

                 except :
                     response_content = "Could not load profile: %s"%file_requested[2]
                
                 #response_content = "setTemps"            

             response_headers = self._gen_headers( 200)
             server_response =  response_headers.encode() # return headers for GET and HEAD

             if (request_method == 'GET'):
                 server_response +=  response_content  # return additional conten for GET only

             conn.send(server_response)
             
             conn.close()

         else:
             print("Unknown HTTP request method:", request_method)
  


def graceful_shutdown(sig, dummy):
    """ This function shuts down the server. It's triggered
    by SIGINT signal """

    run_thread = False
    
    s.shutdown() #shut down the server
    import sys
    sys.exit(1)
###########################################################
#shut down server on ctrl+c

profiles = load_profiles()
signal.signal(signal.SIGINT, graceful_shutdown)
#thread.start_new_thread( run_logger , ("FlowOv",))
print ("Starting web server")
s = Server(81)  # construct server object
s.activate_server() # aquire the socket
