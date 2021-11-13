import pyautogui
import random

class Locations:
    def __init__(self):
        self.locations = {}
        self.imagePath = 'images/'

    def set(self, name, confidence):
        if name not in self.locations:
            result = pyautogui.locateOnScreen(self.imagePath + name + '.PNG', confidence)
            json = self.convertToJson(result) if result else None
            self.locations[name] = json

    def get(self, name, confidence=0.98):
        self.set(name, confidence)
        return self.locations[name]

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

locations = Locations()

def getInventory():    
    return locations.get('inventory')

def getPrayer():
    return locations.get('prayer')

def getRapidHeal():
    
    if prayer:
        position = getPosition(prayer)
        pyautogui.click(position['x'], position['y'])

    return locations.get('rapidHeal')

def getOverload():
    inventory = locations.get('inventory')
    return locations.get('overload')

def getAbsorption():
    return locations.get('absorption')

def getPosition(data):
    x = 0
    y = 0

    for i in range(2):
        x += random.randint(data['x']['low'], data['x']['high'])
        y += random.randint(data['y']['low'], data['y']['high'])
    
    return {
        'x': x / 2,
        'y': y / 2
    }

def getExistsInLocations(name, function):
    if locations.get(name):

    prayer = function() if locations.get(name) else locations['prayer']
