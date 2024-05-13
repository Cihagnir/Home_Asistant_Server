class poo(object) :

  def __init__(self):
    self.coutner = 0 

  
  def counter_incrament(self, foo_obj):

    self.coutner += 1
    foo_obj.counter += 2
    foo_obj.dict_shit["anan"] = self 



class foo(object) :
  
  def __init__(self):
    self.counter = 0
    self.dict_shit = {}


  def deneme(self):
    poo_obj = poo()

    poo_obj.counter_incrament(self)

    print(poo_obj.coutner)
    print(self.counter)
    print(f"Big Shit {self.dict_shit["anan"].coutner}")



foo_obj = foo()

foo_obj.deneme()

