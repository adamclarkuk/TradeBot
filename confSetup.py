import sys
import os
from typing import TextIO
import json

class configfile():

    # All these properties are private and can only be directly accessed
    # with getter and setter methods
    __filehandler = ''  # type: TextIO
    __configuraton = {} # type: Dict {}
    __config_file = "./botconfig.json" # type: string

    def __init__(self, file_location = './botconf.json' ):

        # Set the file location paramater
        self.__config_file = file_location

        #Check if the file exists already, if not create it and load the default settings
        if not os.path.isfile(self.__config_file):

            # Create the file using 'with' so that once we have completed
            # our operations the file will be closed for us automatically
            with open(self.__config_file,'w') as self.__filehandler:
                pass

            # Try to open for file with read/write permission
            if self.open_config_file('r+'):
                # Set the set the default configuration to the new file
                self.default_config()

        # if the file open if with read / write permissions
        else:
            if self.open_config_file('r+'):
                self.load_config()


    def set_file_hanlder(self, file): # Setter method for File Handler

        self.__filehandler = file

    def get_file_Handler(self, file): # Getter for File Handler

        return self.__filehandler

    def default_config(self):

        # Set the configutation dictionary with our default options
        self.__configuration = {  "dronesAllowed": "False",
                                "tradingmode": "sim",
                                "exchanges" : {
                                        "HitBTC" : {
                                            "apikey" : "key value",
                                            "keysecret" : "secret value ",
                                            "URL" : "wss://api.hitbtc.com/api/2/ws",
                                            "maxtokens" : "50" ,
                                            "maxtokensperdrone" : "25"
                                        }
                                    }
                                }

        # Make sure the filehandler has read/write permissions
        if self.__filehandler.mode == 'r+':
            self.save_config()
        else:
            # if not close the file and reopen it
            self.__filehandler.close()
            if self.open_config_file('r+'):
                # Save the configuration to file
                self.save_config()

    def display_current_config(self):

        # Loop through the configuration file
        for key in self.__configuration:

            # Only print the key : pair if self.__configuration[key] is NOT a dictionary
            if isinstance(self.__configuration[key], dict) == False:
                print(key+" : "+str(self.__configuration[key]))

            # Check if the current key is the exchanges
            if key == 'exchanges':
                # Loop through the exchanges
                for exchange_name in self.__configuration[key]:
                    # print the exchange name
                    print("\t"+exchange_name)
                    #Loop through the exchange details and print key : value data
                    for exchange_details in self.__configuration[key][exchange_name]:
                        print("\t\t"+exchange_details+" : "+str(self.__configuration[key][exchange_name][exchange_details]))


    def open_config_file(self,mode): # single function to open the config file

        try:
            self.__filehandler = open(self.__config_file, mode)
        except Exception as error:
            # Print error message
            print("Could not open config file for read/write\n Error was  " + str(error))
            # Exit the script
            sys.exit(0)

        return True

    def load_config(self):

        try:
            self.__configuration = json.load( self.__filehandler )
        
        except Exception as error:
            print("Error Loading configuration")
            print(error)
            sys.exit(0)

    def save_config(self):

        try:
            # Clear file contents first
            self.__filehandler.truncate()
            # Write config dictionary to file
            json.dump(self.__configuration, self.__filehandler)

        except Exception as error:
            print("Error writing to File\n"+error)
            sys.exit(0)



t = configfile()
t.display_current_config()