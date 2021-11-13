import main as bot

def testAll():
    nmz = bot.NMZ()
    assert nmz.getInventory() != None
    assert nmz.getPrayer() != None
    assert nmz.getRapidHeal() != None

testAll()
