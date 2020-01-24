import sys,os
import curses
import requests
from requests import get
from threading import Thread
#Using Clay Mcleod's curses template

get_addr = ""
#data = {'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}
data = {}
run = True


def handle_get():
    global run
    global get_addr
    global data
    while run:
        if get_addr != "":
            try:
                data = get(get_addr, timeout=2).json()
            except Exception:
                pass
            

def draw_menu(stdscr):
    global get_addr
    global data
    k = 0
    cursor_x = 8
    cursor_y = 0
    addr = ""
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('`')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1
        elif k == 127:
            if len(addr) > 0 and cursor_x != 8:
                addr = addr[:cursor_x - 9] + addr[cursor_x - 8:]
                cursor_x -= 1
        elif k in [curses.KEY_ENTER, 10]:
            get_addr = addr
        elif k not in [0,1, ord('ƚ'), ord('`'), ord('Ă'), ord('ă')]:
            if len(addr) + 1 < width-1:
                addr = addr[:cursor_x - 8] + chr(k) + addr[cursor_x - 8:]
                cursor_x += 1

        cursor_x = max(8, cursor_x)
        if cursor_x > min(width-1, 8 + len(addr)):
            cursor_x -= 1


        # Declaration of strings
        keystr = []
        longline = 0
        if data != {}:
            for k,v in data.items():
                #if len(v) > 20
                if len(f"{k}    {v}") > longline:
                    longline = len(f"{str(k)}    {str(v)}")
            for k,v in data.items():
                spacing = " " * ((longline) - (len(str(k)) + len(str(v))))
                keystr.append(f"{k}{spacing}{v}")
                
            start_x_keystr = (int((width // 2) - (len(keystr[0]) // 2) - len(keystr[0]) % 2))        
        else:
            keystr = ['Domain not found']
            start_x_keystr = (int((width // 2) - (len(keystr[0]) // 2) - len(keystr[0]) % 2))        

        if k == 0:
            keystr = "No key press detected..."[:width-1]

        statusbarstr = "Double tap ` to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)

        start_y = 3

        # Rendering some text
        whstr = f"Domain: {addr}"
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)


        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        enum = 0
        if data != {}:
            for s in keystr:
                if start_y + 5 + enum > height - 3:
                    break
                stdscr.addstr(start_y + 5 + 2*enum, start_x_keystr, s)
                enum += 1
                
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    try:
        curses.wrapper(draw_menu)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    request = Thread(target=handle_get)
    request.start()
    main()
    run = False
