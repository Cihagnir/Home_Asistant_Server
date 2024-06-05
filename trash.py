"""
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

"""

import asyncio
import time

is_called = False

async def waitlol():
  is_called = True 
  print("start")
  await asyncio.sleep(5)
  print("finish")


async def main():

  is_called = False
  
  while True :
    print("lol")
    if not is_called:
      asyncio.create_task(waitlol())
      is_called = True
    await asyncio.sleep(1)


asyncio.run(main())

