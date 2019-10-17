
import time
import sys,os
import curses
import keyboard as kb
from random import randint as rn, choice
import ctypes


from pynput.keyboard import Key, Listener
from threading import Thread



global key
key = "=="

global coors
coors = [[], [], [], []]

def on_press(key_pressed):
	global key
	global coors
	if key_pressed:
		key = str(key_pressed)

		if len(coors[0]) != 70:
			while True:
				pos = rn(0, 70)
				if pos not in coors[0]: break

			colors = [29, 35, 41, 3, 11]
			coors[0].append(pos)
			coors[1].append([0, -rn(1, 17)])
			coors[2].append(key)
			coors[3].append(colors[rn(0, len(colors)-1)])

def on_release(key_pressed): pass

def check():
	with Listener(
	        on_press=on_press,
	        on_release=on_release) as listener:
	    listener.join()

t1 = Thread(target=check)

t1.start()

def draw_field(stdscr):
	global key
	global coors

	stdscr.clear()
	stdscr.refresh()
	curses.curs_set(0)

	curses.start_color()
	for k in range(255):
		curses.init_pair(k + 1, k, curses.COLOR_BLACK)

	while True:
		stdscr.clear()

		for y in range(17):
			for x in range(70):
				if x in coors[0]:
					k = coors[0].index(x)
					posit = coors[1][k]
					if posit[1] <= y <= posit[0]:
						if y == posit[0]: color = 85
						elif y == posit[0] - 1: color = 84
						elif y == posit[1]: color = 23
						elif y == posit[1] + 1: color = 29
						else: color = coors[3][k]

						if y == posit[0]: letter = str(coors[2][k])[1]
						else: 
							if rn(0, 1) == 0: letter = chr(choice(
								[rn(48, 123), rn(190, 600)] ))
							else: letter = str(coors[2][k])[1]
						stdscr.addstr(y, x, letter, curses.color_pair(color))
					else:
						stdscr.addstr(y, x, " ")
				else:
					stdscr.addstr(y, x, " ")
		if coors[1] != []:
			n = 0
			for k in range(len(coors[1])): 
				coors[1][k-n][0] += 1
				coors[1][k-n][1] += 1

				if coors[1][k-n][1] >= 17:
					del(coors[0][k-n])
					del(coors[1][k-n])
					del(coors[2][k-n])
					del(coors[3][k-n])

					n += 1

		stdscr.refresh()
		time.sleep(0.07)

def main():
	curses.wrapper(draw_field)

main()
t1.join()