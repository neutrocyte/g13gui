from builtins import property


class DisplayDevice(object):
    """Interface class to support updating displays with.

    Note: Subclasses are expected to override the update method to display each
    frame.
    """

    @property
    def dimensions(self):
        """Return the width and height of the display in pixels.

        returns: a tuple of (x, y)
        """
        raise NotImplementedError('Subclass did not override dimensions!')

    def update(self, image):
        """Update the display with the next frame.

        image: PIL.Image, the next frame to display
        """
        raise NotImplementedError('Subclass did not override update!')
