import os
import ConfigParser

class MyConfigParser(ConfigParser.RawConfigParser):
    """
    """    	   	
    ConfigParser.RawConfigParser.optionxform = str
        
    def valid_items(self, section):
        item_list = ConfigParser.RawConfigParser.items(self, section)
        for item in item_list:
            index = item_list.index(item)
            if not (os.path.exists(item[1]) and os.path.isfile(item[1])):
                item_list.pop(index)
        return item_list


