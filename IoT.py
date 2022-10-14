
import network
import time
import urequests
from machine import Pin ,Timer
from utime import sleep
import ujson
import ntptime
import re


# ubah cron jadi total sec
def cronsim(cron):
    # secs, mins, hours, dayweeks = cron.split(" ")
    cronSplit = cron.split(" ")
    time_in_sec = [1, 60, 6 0 *60, 6 0 *6 0 *24]
    # print(cronSplit)
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

    ret urn total_sec


ntptime.host = "3.id.pool.ntp.org"
SECONDS = 1000

# tim0 = Timer(0)
# Timer(2).init(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:(led_red.off(),print("merah nyala")))

# tim1 = Timer(1)
# tim1.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(1))

# tim2 = Timer(2)
# tim2.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:led_red.on())

url = "http://jsonplaceholder.typicode.com/posts/1"
# url = "http://127.0.0.1:5000/info"

data = {
    "message": "", # str  "timeout": 1, # seconds  "cron": None, # str
}


led_red  = Pin(26,

Pin.OUT)
led_green = Pin(19, Pin.OUT)
led_blue = Pin(5, Pin.OUT)

def changeM(data


,msg,timeout=0, cron =None):
    data['message'] = msg
    data['timeout'] = timeout
    data['cron'] = cron

# delete req


st
def resetM():
    return {
        "message": "", # str  "timeout": 1, # seconds
        "cr  n": None, # str
    }

# print(  ime.localti


())

# Timer(3).init(period=2000, mode=Timer.PERIODIC, callback=lambda t:changeM("on"))
Timer(4).init(period=60000, mode=Timer.PERIODIC, callback=lambda t:changeM(data,"cron", 5 000, "4 * * *  *"))
# changeM("timer", 3000)
# led_blue.on()
# led_red.on()
# Timer(1).init(period=2000, mode=Timer.PERIODIC, callback=lambda t:led_green.on())
# Timer(2).init(period=7000, mode=Timer.PERIODIC, callback=lambda t:led_green.off())
print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

ntptime.settime()
UTC_OFFSET = 8 * 60 * 60  # timezone +8
actua  ime = time.localtime(time.time() + UTC_OFFSET)


res = urequests.get( \

url)
parse = res.json()
prev_data = {}

while True:
    actual_time = time.localtime(time.time() + UTC_OFFSET)
    res = urequests.get(url)
    parse = res.json()
    print(parse)
    # parse = data
    message = parse['message']
    print("berhasil get", parse['message'],actual_time[3],".", actual_time[4], ".", actual_time[5], "me ssage", message)

    if m \
          ssage == "on":
        led_red.on()
        print("relay on")
    elif message == "off":
        led_red.off()
        print("relay off")
    elif message == "timer":
        led_blue.on()
        led_red.on()
        isTimer = True
        timeout = parse['timeout']
        print("timer set")

        Timer(0).init(
            period=timeout,
            mode=Timer.ONE_SHOT,
            callback=lambda t:(
                l ed_red.off(),
                led_blue.off(),
                print("timer timeout, relay off")
            )
        )
        data = resetM()

    # * * * *               secs, mins, hours, dayweeks
    elif message == "cron":
        led_green.on()
        print("cron set")
        timeout = parse['timeout']
        startCron = cronsim(parse['cron'])*1000

        time r Start = Timer(1)
        timerStop = Timer(2).init(period=timeout, mode=Timer.ONE_SHOT, callback=lambda t:(
                                  led_red.on(), pri nt("cron stopped, relay off")))

        timerStart.init(period=startCron, mode=Timer.PERIODIC, callback=lambda t:
                        (led_red.on(), pr int("cron started, relay on"), timerStop))
        data = resetM()
    time.sleep(1)

