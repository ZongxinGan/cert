# -*- coding: utf8 -*-

import ConfigParser


class config_parse():
    def __init__(self,filename):
        self.config_file=filename
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.config_file)

    def get_dbhost(self):
        return self.cf.get("dbconf", "host")
    def get_dbuser(self):
        return self.cf.get("dbconf", "user")
    def get_dbpwd(self):
        return self.cf.get("dbconf", "pwd")
    def get_dbname(self):
        return self.cf.get("dbconf", "db")    
 
    def get_page_num(self):
        return self.cf.getint("pagenumconf", "num")
    def save_page_num(self,done):
        try:
            self.cf.set("pagenumconf", "num", done)
            self.cf.write(open(self.config_file, "w"))
            return 1
        except:
            return 0


if __name__=="__main__":
    a=config_parse('config.ini')

