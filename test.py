import threading
import time
import main as bot

nmz = bot.NMZ()

def testGetInventory():
    assert nmz.getInventory() != None

def testGetPrayer():
    assert nmz.getPrayer() != None

def testRapidHeal():
    assert nmz.getRapidHeal() != None

def testFlickRapidHeal():
    nmz.flickRapidHeal()

def testAll():
    testGetInventory()
    testGetPrayer()
    testRapidHeal()

# testFlickRapidHeal()
# nmz.run()