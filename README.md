# Thinksaber - Turn your laptop into a lightsaber!

## Main Idea

Thinksaber uses the Hard Drive Active Protection System available on
IBM and Lenovo Thinkpad laptops to detect when the laptop is in motion
and make an appropriately giggle-worthy Star Wars-like lightsaber
sound effect.  It was an attempt to teach myself some audio and PyGame
interaction.  This is the result.  Warning: For all I know, this is a
*really bad* thing to do to your hard drive, although I never saw any
problems during testing.  See the "NO WARRANTY GRANTED OR IMPLIED"
line down below.

## Acknowledgements

Thinksaber is obviously inspired by the program MacSaber, and I'm
grateful to the MacSaber people for assembling the Star Wars sound
effects collection needed to make it so successful.

Thinksaber uses a motion-detection algorithm derived from the one
written by Tatsuhiko Miyagawa (miyagawa at gmail.com) for his own
thinkpad-saber program, which ran only under Perl for Windows.
Obviously, I think mine's better.

## Requirements

Thinksaber runs under PyGame, a python-based gaming library, and
should run on any IBM or Lenovo Thinkpad with PyGame installed.  Under
Linux, you may have to activate HDAPS and the joystick device.

## Porting

Thinksaber should run under Windows, but I don't have a Microsoft
Windows installation and so have no idea how to detect the
accelerometer.  Tatsuhiko Miyagawa's perl version is exclusively for
MS Windows, so in theory porting it should be possible.

## NO WARRANTY GRANTED OR IMPLIED

Copyright (C) 2008-2012 Elf M. Sternberg

Thinksaber is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA

	- Elf M. Sternberg <elf@pendorwright.com>
