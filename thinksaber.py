#!/usr/bin/env python
# -*- python -*-
#
#   Thinksaber - Turn your Lenovo Thinkpad into a Jedi weapon!
#   Copyright (C) 2008  Elf M. Sternberg (elf.sternberg@gmail.com)
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Library General Public
#   License as published by the Free Software Foundation; either
#   version 2 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  U

__program__   = "thinksaber.py"
__author__    = "Elf M. Sternberg"
__version__   = "0.3"

import os
import re
import sys
import math
import getopt
import pygame
import random
import string

# global constants

FREQ = 44100 
BITSIZE = -16
CHANNELS = 2
BUFFER = 1024
FRAMERATE = 30


def stddev(ar):
    sumto = sum(ar)
    sumsq = sum([i*i for i in ar])
    return (math.sqrt((len(ar) * sumsq) - (sumto * sumto)) /
            (len(ar)*(len(ar) - 1)))

class Thinksaber:

    def __init__(self, opts = {}):

        self.options = {'swing': 2.0,
                        'strike': 4.5,
                        'hit': 6.0,
                        'path': '.'}

        self.options.update(opts)
        self.foundsound = [i for i in os.listdir(self.options['path'])
                           if i[-4:] in ['.wav', '.mp3']]


    def play(self):

        try:
            pygame.init()
            pygame.joystick.init()
            pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
        except pygame.error, exc:
            raise RuntimeError, "Could not initialize sound system: %s" % exc
    
        
        def gs(m):
            r = [pygame.mixer.Sound(os.path.normpath(
                                    os.path.join(self.options['path'], i)))
                 for i in self.foundsound
                 if re.match(m + r'\d+\.\w{3}$', i)]
            if len(r) < 1:
                raise RuntimeError, "Did not find files for %s sounds." % m
            return r

        sounds = dict([(i, gs(i)) for i in
                       ['start', 'on', 'off', 'idle',
                        'swing', 'strike', 'hit']])
    
        def find_joy():
            for i in xrange(0, pygame.joystick.get_count()):
                joy = pygame.joystick.Joystick(i)
                if joy.get_name().find('HDAPS joystick') != -1:
                    return joy
                if joy.get_name().find('applesmc') != -1:
                    return joy
            raise RuntimeError, "Did not find HDAPS joystick!"

        hdaps = find_joy()
        hdaps.init()
        
        queue = {'x': [hdaps.get_axis(0) for i in xrange(0, 8)],
                 'y': [hdaps.get_axis(1) for i in xrange(0, 8)]}
    
        prev = 0
        up = True
    
        def psound(i):
            sounds[i][random.randint(0, len(sounds[i]) - 1)].play()
    
        try:
            clock = pygame.time.Clock()
            sounds['on'][0].play()
            while pygame.mixer.get_busy():
                clock.tick(FRAMERATE)
    
            idle_channel = pygame.mixer.Channel(0)
            idle_channel.set_endevent(pygame.constants.USEREVENT)
            idle_channel.play(sounds['idle'][0])
    
            while 1:
                event = pygame.event.wait()
                if event.type == idle_channel.get_endevent():
                    idle_channel.play(sounds['idle'][0])
                if event.type == pygame.JOYAXISMOTION:
                    [queue[i].pop(0) for i in queue.keys()]
                    queue['x'].append(hdaps.get_axis(0) * 100)
                    queue['y'].append(hdaps.get_axis(1) * 100)
                    val = max(stddev(queue['x']), stddev(queue['y']))
                    if (up): 
                        if (val > prev):
                            prev = val
                            continue
                        if (val > self.options['hit']):
                            psound('hit')
                        elif (val > self.options['strike']):
                            psound('strike')
                        elif (val > self.options['swing']):
                            psound('swing')
                        up = False
                        continue
                    if (val > prev):
                        prev = val
                        up = True
                        continue
                    prev = val
                    
    
        except KeyboardInterrupt:
            idle_channel.stop()
            sounds['off'][0].play()
            while pygame.mixer.get_busy():
                clock.tick(FRAMERATE)
    
        return 0



def usage(showall = True):
    o = ('-s, --swing=NUMBER     Threshold at which a "swing" sound occurs.',
         '-t, --strike=NUMBER    Threshold at which a "strike" sound occurs.',
         '-h, --hit=NUMBER       Threshold at which a "hit" sound occurs.',
         '-u, --usage            This help.',
         '-v, --version          Version information',
         '',
         'Thresholds are floating point numbers.  The highter the number, ',
         'the harder you have to swing the laptop to get a sound effect. ',
         'Meaningful values are somewhere between 1.0 and 9.0',
         '')

    print 'Thinksaber version %s' % __version__
    if showall:
        print string.join(o, '\n')


    
if __name__ == '__main__':
    tsopts = {}
    opts, args = getopt.getopt(sys.argv[1:], "p:s:t:h:uv",
       ["path=", "swing=", "strike=", "hit=", "usage", "version"])
    for o, a in opts:
        if o in ('-p', '--path'):
            if not os.path.isdir(a):
                raise RuntimeError, '%s is not a directory' % a
            tsopts['path'] = a
        if o in ('-s', '--swing', '-t', '--strike', '-h', '--hit'):
            tsopts[{'s': 'swing',
                    't': 'strike',
                    'h': 'hit'}.get(o.replace('-', ''),
                                    o.replace('-', ''))] = float(a)
        if o in ('-u', '--usage'):
            usage()
            sys.exit(0)

        if o in ('-u', '--usage'):
            usage(False)
            sys.exit(0)
        
    thinksaber = Thinksaber(tsopts)
    thinksaber.play()

