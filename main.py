import configparser
import zmq
import time
import converter
import install

class Microservice:
    """
    Primary loader for the microservice
    """
    def __init__(self):
        """
        Instantiate the launcher, load configs, connect to socket, perform first time setup
        """
        # Fetch the configs
        self._config = configparser.ConfigParser()
        self._config.read('config.ini')
        self._threshold = int(self._config['User Settings']['threshold'])
        self._windows_path = self._config["User Settings"]['windows_path']
        self._target_path = self._config["User Settings"]['target_path']

        # Setup the port to listen to
        context = zmq.Context()
        self._socket = context.socket(zmq.REP)
        self._socket.bind(self._config["User Settings"]['zmq_socket'])
        print("Server is listening on configured port....")
        # If this is the first time being launched, fetch to windows fonts
        if self._config["User Settings"]["first_time"]== 'True':
            self.install(self._windows_path, self._target_path)

        # Listen for requests
        self.main()

    def install(self,windows,target):
        """
        Performs first time setup
        :param windows: the pathway to the windows folder
        :param target: The target pathway for the font files
        """
        # perform first time setups, change first time flag to False
        install.install(windows, target)
        self._config["User Settings"]["first_time"] = 'False'
        with open('config.ini', 'w') as configfile:
            self._config.write(configfile)


    def main(self):
        """
        Continuously listen for a new request
        """
        while True:
            time.sleep(2)
            request = self._socket.recv_json()
            print(f"Server received a request: {request}")
            # Sending a request with a type of quit, will kill the prgram
            if request['type']=='quit':
                break
            self.read_input(request)


    def read_input(self,request):
        """
        Will interpret the request sent via socket and send an appropriate response
        :param request: The request JSON
        """
        try:
            # Fetch the data fields for the request
            type = request['type']
            message = request['message']

            # If the request was to convert, then convert
            if type == 'convert':
                font = request['font']
                size = request['size']
                max_size = request['max_size']

                # Check if the user didn't specifiy specific sizes for non basic fonts
                if size == 'large' and font != 'basic':
                    size = int(self._config['User Settings']['large_size'])
                if size == 'medium' and font != 'basic':
                    size = self._config['User Settings']['medium_size']
                if size == 'small' and font != 'basic':
                    size = self._config['User Settings']['small_size']
                return_message=self.convert_message(message,size,font)

                # If a max size was sent, then we compare the received length to that
                if max_size:
                    # Send an error if the generated chart was too long
                    if len(return_message[0])>max_size:
                        output = {'type': 'error',
                                  'message': f'The length of this message ({len(return_message[0])}) exceeded the max length provided {max_size}'}
                    else:
                        output = {'type': 'matrix',
                                  'message': return_message}
                else:
                    # Send back the generated chart
                    output = {'type':'matrix',
                              'message':return_message}
            else:
                # The request type was invalid
                output = {'type':'error',
                          'message':f"Unrecognized request type: {type}"}
        except KeyError:
            # If the message was missing a key, send back an error
            output = {'type':'error',
                     'message':'Invalid request was sent'}
        print(f"Server is sending back response: {output}")
        self._socket.send_json(output)

    def convert_message(self,message,size,font):
        """
        Generates a chart for a given message
        :param message: The message to be converted
        :param size: The size of the font, numerical or enum of small, medium, large
        :param font: basic or a string which will be searched for in the windows folder
        :return: The generated chart
        """
        phrase = converter.run_conversion(message,size,font,self._threshold,self._target_path)
        return phrase

a = Microservice()