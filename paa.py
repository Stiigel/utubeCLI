#!/usr/bin/python3
"""
Pääjuttu

"""

import kayttoliittyma, sys

kayttoliittyma = kayttoliittyma.Kayttoliittyma()

if "--help" in sys.argv or "--apua" in sys.argv:
  kayttoliittyma.aloita(apu=True)
else:
  kayttoliittyma.aloita()
    
