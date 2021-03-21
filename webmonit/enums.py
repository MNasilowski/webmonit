from enum import Enum

class TimeInterveal(Enum):
    one_min = '1 min'
    five_mins = '5 mins'
    one_hour = '1 hour'

class PageStatus(Enum):
    active = 'Active',
    disabled = 'Disabled'
