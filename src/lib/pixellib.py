"""
Description: This module provides a class to handle a NeoPixel matrix.

Author: Gijs Mos, Sensemakers Amsterdam
Maintainer: Sensemakers Amsterdam  https://sensemakersams.org

Classes:
- NeoPixMatrix: A class to handle a NeoPixel matrix with various utility methods.

Methods:
- __init__(self, neo_pixels, n_cols, n_rows, n_start=0): Initialize the NeoPixMatrix.
- _row_col_to_n(self, row, col): Convert row and column to a single index.
- set_pix(self, row, col, color=(0, 0, 0), show=False): Set the color of a specific pixel.
- set_index(self, index, color=(0, 0, 0), show=False): Set the color of a specific pixel by index.
- set_row(self, row, color=(0, 0, 0), show=False): Set the color of an entire row.
- set_col(self, col, color=(0, 0, 0), show=False): Set the color of an entire column.
- clear(self, show=True): Clear the entire matrix by setting all pixels to the clear color.
- write(self): Update the display.
- size(self): Return the total number of pixels in the matrix.
"""

import neopixel
from gfx import GFX
from time import sleep_ms
from machine import Pin

class NeoPixMatrix(GFX):
    BLUE = (0, 0, 255)
    CLEAR = (0, 0, 0)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    def __init__(self, neo_pixels, n_cols, n_rows, n_start=0):
        """Initialize the NeoPixMatrix.

        Args:
            neo_pixels (neopixel.NeoPixel): The NeoPixel matrix.
            n_cols (int): The number of columns in the matrix.
            n_rows (int): The number of rows in the matrix.
            n_start (int): The first pixel to be used for this matrix (default 0).
        Returns:
            None
        """
        super().__init__(n_cols, n_rows, self.set_pix)
        # Check the construction arguments
        assert isinstance(neo_pixels, neopixel.NeoPixel), "No NeoPixel matrix passed."
        assert 0 < n_rows <= 100, f"Illegal n_rows: {n_rows}."
        assert 0 < n_cols <= 100, f"Illegal n_cols: {n_cols}."
        # assert n_rows * n_cols == neo_pixels.n, "N rows/cols does not match matrix."
        # Set our attributes.
        self.pix = neo_pixels
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_start = n_start

    def _row_col_to_n(self, row, col):
        """Convert row and column to a single index.

        Args:
            row (int): The row index.
            col (int): The column index.

        Returns:
            int: The single index corresponding to the row and column.
        """
        return (col * self.n_rows + row) + self.n_start

    def set_pix(self, row, col, color=(0, 0, 0), show=False):
        """Set the color of a specific pixel.

        Args:
            row (int): The row index of the pixel.
            col (int): The column index of the pixel.
            color (tuple, optional): The color to set the pixel to. Defaults to (0, 0, 0).
            show (bool, optional): Whether to update the display immediately. Defaults to False.

        Returns:
            None
        """
        if row < 0 or col < 0 or row >= self.n_rows or col >= self.n_cols:
            return
        # print(f" set ({col}, {row}) to {color}")
        self.pix[self._row_col_to_n(row, col)] = color
        if show:
            self.write()

    def set_index(self, index, color=(0, 0, 0), show=False):
        """Set the color of a specific pixel.

        Args:
            index (int): The index of the pixel.
            color (tuple, optional): The color to set the pixel to. Defaults to (0, 0, 0).
            show (bool, optional): Whether to update the display immediately. Defaults to False.

        Returns:
            None
        """
        self.pix[index + self.n_start] = color
        if show:
            self.write()

    def set_row(self, row, color=(0, 0, 0), show=False):
        """Set the color of an entire row.

        Args:
            row (int): The row index.
            color (tuple, optional): The color to set the row to. Defaults to (0, 0, 0).
            show (bool, optional): Whether to update the display immediately. Defaults to False.

        Returns:
            None
        """
        for c in range(self.n_cols):
            self.set_pix(row, c, color)
        if show:
            self.write()

    def set_col(self, col, color=(0, 0, 0), show=False):
        """Set the color of an entire column.

        Args:
            col (int): The column index.
            color (tuple, optional): The color to set the column to. Defaults to (0, 0, 0).
            show (bool, optional): Whether to update the display immediately. Defaults to False.

        Returns:
            None
        """
        for r in range(self.n_rows):
            self.set_pix(r, col, color)
        if show:
            self.write()

    def clear(self, show=True):
        """Clear the entire matrix by setting all pixels to the clear color.

        Args:
            show (bool, optional): Whether to update the display immediately. Defaults to True.

        Returns:
            None
        """
        if 0 == self.n_start:
            self.pix.fill(self.CLEAR)
        else:
            for i in range(self.size()):
                self.set_index(i, self.CLEAR)
        if show:
            self.write()

    def write(self):
        self.pix.pin.off()
        sleep_ms(1)
        self.pix.write()

    def size(self):
        return self.n_rows * self.n_cols
