import machine
from wifi_manager import WifiManager
import utime
import coin

# Example of usage
coin.bill_last_state = 0
coin.bill_pulse_count = 0 
coin.total = 0
pin_coin =  machine.Pin(4, machine.Pin.IN)
pin_coin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=coin.coin_callback)


wm = WifiManager()
wm.connect()
while True:
    if wm.is_connected():
        print('Connected!')
        led = machine.Pin(2, machine.Pin.OUT)
    else:
        print('Disconnected!')
    utime.sleep(10)
