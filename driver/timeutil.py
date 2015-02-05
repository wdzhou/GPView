################################################################################
#
# Alarm clock
#
################################################################################
import sys
import datetime
import time
import pytz

TIMEZONE = 'Asia/Shanghai'


def getTimeZone(timezonestr):
    """ Return the time zone object
    """
    mytimezone = pytz.timezone(timezonestr)

    return mytimezone



def getNow(tz):
    """ Get current time in 24 hour format
    Argument:
     - tz : time zone 
    """
    now = datetime.datetime.now(tz)
   
    today = str(now).split()[0]
    timenow = datetime.time(now.hour, now.minute)

    return today, timenow


def checkInitialAlarmStatus(timezone, alarms, statusPassed):
    """ 
    """
    currtime = getNow(timezone)

    for ialarm in xrange(len(alarms)):
        alarm = alarms[ialarm]
        if alarm <= currtime:
            print "Alarm %s is due! Now is %s" % (str(alarm), str(currtime))
            statusPassed[ialarm] = True
        else:
            statusPassed[ialarm] = False
    # ENDFOR()

    return


def doAlarm(time1, timenow):
    """
    """
    diffhour = timenow.hour - time1.hour
    diffmin = timenow.minute - time1.minute
    diffsecond = diffhour * 60 + diffmin

    wbuf = "\tBeep.... for alarm @ %s.  Due by %d minutes \n" % (str(time1), diffsecond)

    return wbuf

def startAlarms(alarms, statusPassed, statusAlarmed, mytimezone):
    """
    """
    SLEEPTIME = 1

    ticking = True
    while ticking is True:
        timenow = getNow(mytimezone)
        info = ""
        for ia in xrange(len(alarms)):
            if statusPassed[ia] is True and statusAlarmed[ia] is False:
                info += doAlarm(alarms[ia], timenow)
                statusAlarmed[ia] = True
            elif statusPassed[ia] is False and alarms[ia] <= timenow:
                info += doAlarm(alarms[ia], timenow)
                statusPassed[ia] = True
                statusAlarmed[ia] = True
        # ENDFOR

        # Output
        if info != "":
            print "@ Time = %s\n%s" % (str(timenow), info)
        
        time.sleep(SLEEPTIME)
    # ENDWHILE

    return


def main(argv):
    """ Set up daily alarm
    """
    # Process inputs
    if len(argv) == 0:
        print "Something wrong!"
        exit(2)
    elif len(argv) == 1:
        print "Input: %s [HH:MM 1] [HH:MM 2] ... " % (argv[0])
        exit(2)

    alarms = []
    for argc in xrange(1, len(argv)):
        timestr = argv[argc]
        terms = timestr.split(":")
        hour = int(terms[0])
        minute = int(terms[1])
        alarm = datetime.time(hour, minute)
        alarms.append(alarm)

    # Set up
    mytimezone = getTimeZone(TIMEZONE)

    isANewDay = True 
    
    statusPassed = []
    statusAlarmed = []
    for ia in xrange(len(alarms)):
        statusPassed.append(None)
        statusAlarmed.append(False)

    # Set up init status of all alarms
    checkInitialAlarmStatus(mytimezone, alarms, statusPassed)

    for i in xrange(len(alarms)):
        print "Alarm @ %s is due ??? %s" % (str(alarms[i]), statusPassed[i])


    # Run into alarm
    startAlarms(alarms, statusPassed, statusAlarmed, mytimezone)

    return


if __name__ == "__main__":
    main(sys.argv)
