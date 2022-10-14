
import network
import time
import urequests
from machine import Pin ,Timer
import utime
import ujson
import ntptime
import re

# simulation
def getInfo():
    return dataList[0]

def delete():
    if len(dataList) != 1:
        dataList.pop(0)
    else:
        dataList[0 ]= firstData
    return dataList

def setTimer(timeout):
    data = {
        "message": "timer",
        "timeout": int(timeout),
        "cron": None,
    }
    data2 = {
        "message": "on",
        "timeout": 0,
        "cron": None,
    }
    if len(dataList) != 1:
        dataList[0] = data

    else:
        dataList.insert(0, data)
    dataList[1] = data2
    return data

def setCron(cron, timeout):
    data = {
        "message": "cron",
        "timeout": int(timeout),
        "cron": cron,
    }
    data2 = {
        "message": "off",
        "timeout": 0,
        "cron": None,
    }
    if len(dataList) != 1:
        dataList[0] = data

    else:
        dataList.insert(0, data)
    dataList[1] = data2
    return data

def on():
    data = {
        "message": "on",
        "timeout": 0,
        "cron": None,
    }
    dataList[0] = data
    return data

def off():
    data = {
        "message": "off",
        "timeout": 0,
        "cron": None,
    }
    dataList[0] = data
    return data

# ubah cron jadi total sec
def cronsim(cron):
    # secs, mins, hours, dayweeks = cron.split(" ")
    cronSplit = cron.split(" ")
    time_in_sec = [1, 60, 6 0 *60, 6 0 *6 0 *24]
    i = 0
    total_sec = 0
    isStar = False
    isNum = False
    for c in cronSplit:
        if c == "*" and (not isStar) and (not isNum):
            total_sec += time_in_sec[i]
            isStar = True
        elif re.match(r"^([1-9]|[1-5][0-9]|60)$", c):
            if isStar:
                total_sec = 0
                isStar = False
            total_sec += int(c) * time_in_sec[i]
            isNum = True i+=1

    r eturn total_sec


# Initialize
ntptime.host = "3.id.pool.ntp.org"

url = "https://flaskrelayiot.alzifoztran.repl.co/info"

data = {
    "message": "", # str
    "timeout": 1, # secon  s
    "cron": None, # str
}

dataList = []

firstData = {
    "message": "off",
    "timeout": 0,
    "cron": None,
}

dataList.append(firstData)

led_red = Pin(26, Pin.OUT)
led_green = Pin(19, Pin.OUT)
led_blue = Pin(5, Pin.OUT)

SECONDS = 500

# print(time.localtime())

# Setup
print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

ntptime.settime()
UTC_OFFSET = 8 * 60 * 60  # tim  ne +8
actual_time = time.localtime(time.time() + UTC_OFFSET)

# tes


/off
# Timer(1).init(period=3*SECONDS, mode=Timer.ONE_SHOT, callback=lambda t:(on(), print("on")))
# Timer(2).init(period=7*SECONDS, mode=Timer.ONE_SHOT, callback=lambda t:(off(), print("of")))


# tes timer
# setTimer(5 * SECONDS)

# tes cron
# setCron("5 * * *", 5 * SECONDS)


def run():
    actual_time = time.localtime(time.time() + UTC_OFFSET)
    print("send request")
    res = urequests.get(url)
    parse = res.json()
    # res = getInfo()
    # parse = res
    message = parse['message']
    print("berhasil get", parse['message'],actual_t ime[3],".",actu al_t ime[4],".",actu al_t ime[5], "message", message)

    if message == "on":
        led_red.on()
        print("relay on")
    elif message == "off":
        led_red.off()
        print("relay off")
    elif message == "timer":
        led_blue.on()
        led_red.on()
        timeout = parse['timeout']
        print("timer set")

        Timer(0).init(
            period=timeout,
            mode=Timer.ONE_SHOT,
            callback=lambda t:(
                led_red.off(),
                # off(),
                led_blue.off(),
                print("timer timeout, relay off")
            )
        )
        urequests.post("https://flaskrelayiot.alzifoztran.repl.co/delete")
        # delete()

    # * * * *               secs, mins, hours, dayweeks
    elif message == "cron":
        led_green.on()
        print("cron set")
        timeout = parse['timeout']
        startCron = cronsim(parse['cron'])*1000

        timerStart = Timer(1)
        timerStop = Timer(2).init(
            period=timeout,
            mode=Timer.ONE_SHOT,
            callback=lambda t:(
                led_red.off(),
                # off(),
                print("cron stopped, relay off")
            )
        )

        timerStart.init(
            period=startCron,
            mode=Timer.PERIODIC,
            callback=lambda t:(
                led_red.on(),
                print("cron started, relay on"),
                timerStop
            )
        )
        urequests.post("https://flaskrelayiot.alzifoztran.repl.co/delete")
        # delete()



# LOOP


Timer(10).init(period=500, mode=Timer.PERIODIC, callback=lambda t:(run() ))

while True:
    run()
    time.sleep(1)