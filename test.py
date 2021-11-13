import main as bot

def testAll():
    assert bot.getInventory() != None
    assert bot.getPrayer() != None
    assert bot.getRapidHeal() != None

testAll()
