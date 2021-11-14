import threading
import pyautogui
import random
import time
from datetime import datetime

MILLISECOND = 1
SECOND = MILLISECOND * 1000
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24

class Logs:
    def __init__(self):
        self.logs = []

    def log(self, message):
        now = datetime.now()
        currentTime = now.strftime("%H:%M:%S")
        self.logs.append(currentTime + ' : ' + message)

        print(self.logs[-1])

    def getLogs(self):
        return self.logs

log = Logs().log        

class Locations:
    def __init__(self):
        self.locations = {}
        self.imagePath = 'images/'

    def set(self, name, confidence):
        if name not in self.locations or not self.locations[name]:
            result = pyautogui.locateOnScreen(self.imagePath + name + '.PNG', confidence)
            json = self.convertToJson(result) if result else None
            self.locations[name] = json
            log('Setting ' + name + ', with confidence: ' + str(confidence))

    def get(self, name, confidence=0.98):
        self.set(name, confidence)
        log('Getting ' + name + ', with confidence: ' + str(confidence))
        return self.locations[name]

    def clear(self, name):
        self.locations[name] = None
        log('Clearing ' + name)

    def convertToJson(self, data):
        json = {}

        json['x'] = {
            "low": data.left,
            "high": data.left + data.width
        }
        json['y'] = {
            "low": data.top,
            "high": data.top + data.height
        }

        return json

class setInterval:
    def __init__(self, action, time):
        self.time = time / 1000
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self._setInterval)
        thread.start()

    def setTimeOut(self):
        nextTime = time.time() + self.time
        self.stopEvent.wait(nextTime-time.time())
        self.action()

    def _setInterval(self):
        nextTime = time.time() + self.time
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime += self.time
            self.action()

    def cancel(self):
        self.stopEvent.set()

class Names:
    def __init__(self):    
        self.INVENTORY = 'inventory'
        self.PRAYER = 'prayer'
        self.RAPID_HEAL = 'rapidHeal'
        self.OVERLOAD = 'overload'
        self.ABSORPTION = 'absorption'

class NMZ:
    def __init__(self):
        self.locations = Locations()
        self.names = Names()
        self.queue = []
        self.terminated = False

    def run(self):
        self.clock()

        while not self.terminated:
            while len(self.queue):
                action = self.queue.pop(0)
                action()
                time.sleep(0.5)

            time.sleep(5)

        log('Terminated')

    def debug(self):
        self.clock()

        while not self.terminated:
            inp = input("input: ")
            action = self.queue.pop(0)
            action()
            print('performing:', action.__name__)

    def execute(self, action):
        self.queue.append(action)
        log('Queueing: ' + action.__name__)

    def clock(self):
        drinkOverload = setInterval(lambda: self.execute(self.drinkOverload), 5 * SECOND)
        flickRapidHeal = setInterval(lambda: self.execute(self.flickRapidHeal), 2 * SECOND)                

    def tick(self):
        t = random.randrange(450, 650)
        time.sleep(t / 1000)

    # if no more overload we should exit the bot
    def drinkOverload(self):
        loc = self.getOverload()

        if not loc:
            self.terminated = True
            return

        self.clickExists(loc)

    def flickRapidHeal(self):
        loc = self.getRapidHeal()
        self.clickExists(loc)
        self.tick()
        self.clickExists(loc)

    def getInventory(self):    
        return self.locations.get()

    def getPrayer(self):
        prayerLoc = self.locations.get(self.names.PRAYER)
        return prayerLoc

    def getRapidHeal(self):
        loc = self.locations.get(self.names.PRAYER)
        self.clickExists(loc)
        rapidHealLoc = self.locations.get(self.names.RAPID_HEAL)
        self.locations.clear(self.names.RAPID_HEAL)
        return rapidHealLoc

    def getOverload(self):
        loc = self.locations.get(self.names.INVENTORY)
        self.clickExists(loc)
        return self.locations.get(self.names.OVERLOAD, confidence=0.8)

    def getAbsorption(self):
        loc = self.locations.get(self.names.INVENTORY)
        self.clickExists(loc)
        return self.locations.get(self.names.ABSORPTION)

    def getPositionToClick(self, data):
        x = 0
        y = 0

        for i in range(2):
            x += random.randint(data['x']['low'], data['x']['high'])
            y += random.randint(data['y']['low'], data['y']['high'])
        
        return {
            'x': x / 2,
            'y': y / 2
        }

    def clickExists(self, loc):
        if loc:
            position = self.getPositionToClick(loc)
            pyautogui.click(position['x'], position['y'])
