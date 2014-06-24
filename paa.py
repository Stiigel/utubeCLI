#!/usr/bin/python3
"""
Pääjuttu

"""

import kayttoliittyma, sys

kayttoliittyma = kayttoliittyma.Kayttoliittyma()

apu = False
if "--help" in sys.argv or "--apua" in sys.argv:
  apu = True

kayttoliittyma.aloita(apu=apu)
    
