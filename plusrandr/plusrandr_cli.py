#!/usr/bin/env python2

from plusrandr_core import PlusRandR


class PlusRandRCli:
    def __init__(self):
        self._simpledR = PlusRandR()

        self._mirror_button_status = "grayed out"
        self._screen1_status = "active"
        self._screen2_status = "grayed out"
        self._nb_screens = self._simpledR.get_nb_outputs()

        self.update_gui()

    def update_gui(self):
        if self._nb_screens == 2:
            self._mirror_button_status = "active"
            self._screen2_status = "active"
        elif self._nb_screens == 1:
            self._mirror_button_status = "grayed out"
            self._screen2_status = "grayed out"

    def run(self):
        print "commands: refresh, status, mirror, set1, set2"
        while True:
            # cntrl-c to quit
            self._simpledR.refresh_xrandr()
            self._nb_screens = self._simpledR.get_nb_outputs()
            cli_input = raw_input('your_prompt$ ')
            cli_input = cli_input.split()
            if cli_input[0] == 'refresh':
                self._nb_screens = self._simpledR.refresh_xrandr()
            elif cli_input[0] == 'status':
                self.print_status()
            elif cli_input[0] == 'mirror':
                if self._nb_screens == 2:
                    self._simpledR.mirror_screens()
                else:
                    print "grayed out"
            elif cli_input[0] == 'set1':
                if self._nb_screens == 2:
                    self._simpledR.set_single_screen(0)
                else:
                    print "only one screen connected, that one!"
            elif cli_input[0] == 'set2':
                if self._nb_screens == 2:
                    self._simpledR.set_single_screen(1)
                else:
                    print "grayed out"
            else:
                print "didnt get this"

    def print_status(self):
        print "button 1 %s" % self._mirror_button_status
        print "button 2 %s" % self._screen1_status
        print "button 3 %s" % self._screen2_status


mymain = PlusRandRCli()
mymain.run()
