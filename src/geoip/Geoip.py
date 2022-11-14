
import pickle
import os
import pathlib

class Geoip:
    
    def __init__(self, file=None):
        try:
            if file and os.path.isfile(file):
                path = os.path.abspath(file)
                
                
            elif file == None:
                path = pathlib.Path(__file__).parent.resolve()
                path = os.path.join(path, 'geoip.bin')
                
            else:
                print("nothing works here")
                exit()
            
            with open(path, 'rb') as fp:
                self.data = pickle.load(fp)
                
        except Exception as e:
            print("could not find geoip data")
            print(pathlib.Path(__file__).parent.resolve())
            print(e)
            exit()
            self.data = None
            
    def test(self):
        print()
        print("test..")
        if self.data:
            print(len(self.data))
            print(self.data[0])
            print(self.data[1000])
            print(self.data[10000])
            print()
        else:
            print("no data found..")
    
    def ip_int(self, ip:str) -> int:
        a3,a2,a1,a0 = ip.split('.')
        a3,a2,a1,a0 = int(a3),int(a2),int(a1),int(a0)
        return 256**3*a3 + 256**2*a2 + 256*a1 + a0
            
    def search(self, ip):
        int_ip = self.ip_int(ip)
        
        for data in self.data:
            if int_ip >= data['start'] and int_ip <= data['stop']:
                return data
                #return {"code": data['code'], "country": data['country']}
            
        return None
    
    
if __name__ == "__main__":
    ## test it..
    geoip = Geoip()
    geoip.test()
    print(geoip.search("61.177.173.39"))
    
    
    