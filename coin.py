from machine import Pin
from time import time

# Global variables
pulse_count = 0
pulse_last_state = 0
pulse_state = 0
money_in_session = 0
time_last_pulse = 0


bill_pulse_count = 0
bill_last_state = 0 
total = 0

def coin_callback(p):
    global bill_pulse_count, bill_last_state, total
    pulse_state = p.value()
    if pulse_state == 0 and bill_last_state == 0 :  #// this means we entered a new pulse
        bill_last_state = 1 #// set the previous state
    elif pulse_state == 1 and bill_last_state == 1: #// this means a pulse just ended
        bill_last_state = 0
        bill_pulse_count = bill_pulse_count +1  #// increment the pulse counter
        total = bill_pulse_count * 1
        # mqtt_pub.pub(b"coin","1")
        #mqtt_pub.pub(b"total",str(bill_pulse_count))
    print('bill_last_state',pulse_state, "total money", total, "bill_pulse_count", bill_pulse_count) 

def pulse_counter(pin, new_coin):
    """
    Counts the pulses and updates the pulse count.

    Args:
        pin (Pin): The input pin connected to the pulse signal.
        new_coin (bool): Indicates if a new coin is introduced.

    Returns:
        int: The updated pulse count.
    """
    global pulse_count
    global pulse_last_state

    pulse_state = pin.value()

    if pulse_state == 0 and pulse_last_state == 0:  # New pulse detected
        pulse_last_state = 1
        if new_coin:
            pulse_count = 0
    elif pulse_state == 1 and pulse_last_state == 1:  # Pulse ended
        pulse_last_state = 0
        pulse_count += 1

    return pulse_count


def check_for_new_coin(time_last_pulse, time_now):
    """
    Checks if a new coin is introduced based on the time elapsed since the last pulse.

    Args:
        time_last_pulse (float): The timestamp of the last pulse.
        time_now (float): The current timestamp.

    Returns:
        bool: True if a new coin is introduced, False otherwise.
    """
    if time_last_pulse != 0:
        if time_now - time_last_pulse > 1:  # Assuming 1 second as the threshold for a new coin
            print("New coin time")
            return True
        else:
            print("Same coin time")
            return False
    else:
        print("time_last_pulse EQ 0")
        return False


def save_money_in_session(pulse_state, pulse_count, money_in_session):
    """
    Saves the money introduced in the current session based on the pulse state.

    Args:
        pulse_state (int): The state of the pulse.
        pulse_count (int): The count of pulses.
        money_in_session (float): The amount of money in the current session.

    Returns:
        float: The updated money in session.
    """
    if pulse_state == 1:
        money_by_pulses, money_in_session = pulse_money_equivalences(pulse_count, money_in_session)
        print("pulse_last_state:", pulse_state)
        print("pulse_count:", pulse_count)
        print("money_by_pulses:", money_by_pulses)
        print("money_in_session:", money_in_session)
    return money_in_session


def pulse_money_equivalences(total_pulses, money_in_session):
    """
    Given a total number of pulses, returns the equivalent money value based on hardcoded rules.

    Args:
        total_pulses (int): The total number of pulses to convert to a money value.
        money_in_session (float): The amount of money in the current session.

    Returns:
        tuple: A tuple containing the money earned by pulses and the updated money in session.
    """
    if total_pulses == 5:
        money = 1
        money_in_session += money
    elif total_pulses == 6:
        money = 2
        money_in_session += money - 1
    elif total_pulses == 7:
        money = 5
        money_in_session += money - 2
    elif total_pulses == 8:
        money = 10
        money_in_session += money - 5
    else:
        money = 0

    return money, money
