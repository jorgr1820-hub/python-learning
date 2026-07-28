class phone:
    def __init__(self,brand):
        self.brand = brand
        self.battery = 100  
    
    def use(self):
        try:        
            if self.battery > 0:
                self.battery -= 10
            else:
                raise Exception ("Battery is empty")
        except Exception:       
            print("Battery is empty")
        print(f"Battery level: {self.battery}%")

    
    def charge(self):
        try:
            if self.battery < 100:
                self.battery +=20
            else:
                raise Exception ("Battery is full")
        except Exception:
            print("Battery is full")
        print(f"Battery level: {self.battery}%")



phone1 = phone("iPhone")
phone1.use()
phone1.use()
phone1.use()
phone1.use()
phone1.use()
phone1.use()
phone1.use()
phone1.use()
phone1.use()
phone1.use()
phone1.use()       
