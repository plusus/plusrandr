from screenlayout.xrandr import XRandR
from screenlayout.auxiliary import Position, NORMAL, NamedSize


class PlusRandR:
    def __init__(self):
        self._xrandr = XRandR()
        self._highest_common_res = None
        """:type: NamedSize"""
        self._plugged_outputs = []
        """:type: List[str]"""
        self.refresh_xrandr()

    def refresh_xrandr(self):
        """ Gets screen info from xrandr"""
        self._xrandr.load_from_x()
        # Get resolutions of connected screens
        so = self._xrandr.state.outputs
        self._plugged_outputs = [a for a in so.iterkeys() if so[a].connected]
        if len(self._plugged_outputs) == 2:
            self._highest_common_res = [x for x in so[self._plugged_outputs[0]].modes
                                        for y in so[self._plugged_outputs[1]].modes if
                                        str(x) == str(y)][0]

    def get_nb_outputs(self):
        """ Gets number of connected screens (not necessarily active)"""
        return len(self._plugged_outputs)

    def mirror_screens(self):
        """ Mirrors 2 screens, does nothing with 1 screen"""
        if len(self._plugged_outputs) == 2:
            for key in self._plugged_outputs:
                self.set_config_screen(self._xrandr.configuration.outputs[key], self._highest_common_res)

            self._xrandr.save_to_x()

    def set_single_screen(self, screen_inx):
        """
        Enable screen at index screen_inx with max resolution, disable the other one
        If there is only 1 screen, always set screen 0 at max available resolution
        :type screen_inx: bool
        """
        def set_config_default(inx):
            self.set_config_screen(self._xrandr.configuration.outputs[self._plugged_outputs[inx]],
                                   self._xrandr.state.outputs[self._plugged_outputs[inx]].modes[0])

        if len(self._plugged_outputs) == 2:
            screen1, screen2 = (1, 0) if screen_inx else (0, 1)
            set_config_default(screen1)
            self._xrandr.configuration.outputs[self._plugged_outputs[screen2]].active = False
        else:
            set_config_default(0)
        self._xrandr.save_to_x()

    def set_config_screen(self, config_screen, resolution, active=True, position=Position((0, 0)), rotation=NORMAL):
        """ Set screen configuration parameters on the config_screen passed"""
        setattr(config_screen, "mode", resolution)
        config_screen.position = position
        config_screen.rotation = rotation
        config_screen.active = active
