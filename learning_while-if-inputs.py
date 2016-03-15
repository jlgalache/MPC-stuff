#!/usr/bin/env python3
# -*- coding: utf-8 -*-

question = " Do you want to print a message onscreen? Ans: "
cont = 1

while cont == 1:
  reply = str.casefold(input(question))
  if reply == 'yes' or reply == 'y':
    print(" Hello, cruel World!")
    cont = 0
  elif reply == 'no' or reply == 'n':
    print(" Fine, suit yourself!")
    cont = 0
  elif reply == '':
    print("\n I'm sorry, did you forget to tpye a reply,\n or could you just not give a toss?\n Either way, please input a response.")
    question = " I'll wait... Ans: "
    cont = 1
  
