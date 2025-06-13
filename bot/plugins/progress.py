from math import floor
from pyrogram.types import Message, MessageEntity

def get_progress_text(name,status,completed,speed,total,enco=False):
    text = """Name: {}
{}: {}%
⟨⟨{}⟩⟩
{} of {}
Speed: {}
ETA: {}
    """

    text2 = """Name: {}
{}: {}%
⟨⟨{}⟩⟩
Speed: {}
ETA: {}
    """

    if enco == False:
        total = str(total)
        completed = round(completed*100,2)
        size, forma = total.split(' ')
        if forma == "MiB":
            size = int(round(float(size)))
        elif forma == "GiB":
            size = int(round(float(size)*1024,2))

        percent = completed
        speed = round(float(speed)/1024) #kbps

        if speed == 0:
            speed = 0.1

        ETA = round((size - ((percent/100)*size))/(speed/1024))

        if ETA > 60:
            x = floor(ETA/60)
            y = ETA-(x*60)

            if x > 60:
                z = floor(x/60)
                x = x-(z*60)
                ETA = str(z) + " Hour " + str(x) + " Minute"
            else:
                ETA = str(x) + " Minute " + str(y) + " Second"
        else:
            ETA = str(ETA) + " Second"  

        if speed > 1024:
            speed = str(round(speed/1024)) + " MB"
        else:
            speed = str(speed) + " KB"

        completed = round((percent/100)*size)

        if completed > 1024:
            completed = str(round(completed/1024,2)) + " GB"
        else:
            completed = str(completed) + " MB"

        if size > 1024:
            size = str(round(size/1024,2)) + " GB"
        else:
            size = str(size) + " MB"

        fill = "▪️"
        blank = "▫️"
        bar = ""

        bar += round(percent/10)*fill
        bar += round(((20 - len(bar))/2))*blank


        speed += "/sec"
        text = text.format(
            name,
            status,
            percent,
            bar,
            completed,
            size,
            speed,
            ETA
        )
        return text

    elif enco == True:
        speed = float(speed)
        if speed == 0:
            speed = 0.01

        remaining = floor(int(total)-completed)
        ETA = floor(remaining/float(speed))

        if ETA > 60:
            x = floor(ETA/60)
            y = ETA-(x*60)

            if x > 60:
                z = floor(x/60)
                x = x-(z*60)
                ETA = str(z) + " Hour " + str(x) + " Minute"
            else:
                ETA = str(x) + " Minute " + str(y) + " Second"
        else:
            ETA = str(ETA) + " Second"

        percent = round((completed/total)*100,2)

        fill = "▪️"
        blank = "▫️"
        bar = ""

        bar += round(percent/10)*fill
        bar += round(((20 - len(bar))/2))*blank
        
        speed = str(speed) + "x"

        text2 = text2.format(
            name,
            status,
            percent,
            bar,
            str(speed),
            ETA
        )
        return text2
