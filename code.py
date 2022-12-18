from time import sleep
import circuitpython_schedule as schedule
import board
import digitalio
import displayio
import neopixel

display = board.DISPLAY

bitmap = displayio.Bitmap(160, 128, 1)
tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

group = displayio.Group()
group.append(tile_grid)

display.show(group)
display.brightness = 0

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import AudioOut
    except ImportError:
            print("This board does not seem to support audio playback :(")

speaker = AudioOut(board.SPEAKER)
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)

speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

startup_wave_file = open("startup.wav", "rb")
startup_wave = WaveFile(startup_wave_file)

speaker.play(startup_wave)
sleep(1.5)

speaker.deinit()
speaker_enable.value = False

string1 = digitalio.DigitalInOut(board.A0)
string2 = digitalio.DigitalInOut(board.A1)

string1.direction = digitalio.Direction.OUTPUT
string2.direction = digitalio.Direction.OUTPUT

# def blink_string():
#     string1.value = 1
#     string2.value = 1
#     sleep(1)
#     string1.value = 0
#     string2.value = 0


neopixel_count = 5
neopixel_order = neopixel.GRB
neopixels = neopixel.NeoPixel(board.D8, neopixel_count, brightness=0.05, pixel_order=neopixel_order)

#schedule.every(1).seconds.do(blink_string)

def wheel(pos):

    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos *  3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170 :
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r =0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if neopixel_order in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def rainbow_cycle():
    for j in range(255):
        schedule.run_pending()
        for i in range(neopixel_count):
            pixel_index = (i * 256 // neopixel_count) + j
            neopixels[i] = wheel(pixel_index & 255)
        neopixels.show()

print("\nHello there! :)")


#sleep(1)
print("\n- Your Christmas lights connected to pins A0 and A1 are now up and running. The output voltage is ~2.8 Volts.")
#sleep(4)
#print("\n- Please note that this system was only tested  with IKEA Stråla         Christmas lights with   12 LEDs. Normally,      these use 2 AA batteries(1.5 Volts each).")
#sleep(4)
#print("\n- The display will turn off in 10 seconds in    order to save power and prevent burn-in.")
#sleep(10)

string1.value = 1
string2.value = 1

while True:
    rainbow_cycle()