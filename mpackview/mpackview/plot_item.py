#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 mjbots Robotic Systems, LLC.  info@mjbots.com
# Copyright 2024 Inria
#
# This file incorporates code from utils/gui/moteus_gui/tview.py
# (https://github.com/mjbots/moteus, 49c698a63f0ded22528ad7539cc2e27e41cd486d)

"""Data associated with a plot."""

import time
from typing import List

import matplotlib

from .plot_callback import PlotCallback


class PlotItem(object):
    """Data associated with a plot.

    Attributes:
        COLORS: Successive plot colors, as a string of color-code characters.
        xdata: Matplotlib x-axis data.
        ydata: Matplotlib y-axis data.
    """

    COLORS = "rbgcmyk"
    xdata: List[float]
    ydata: List[float]

    def __init__(self, axis, plot_widget, name, callback: PlotCallback):
        """Initialize plot item.

        Args:
            axis: Matplotlib axis.
            plot_widget: Parent plot widget.
            name: Plot label.
            callback: Callback handle.
        """
        self.axis = axis
        self.connection = callback.connect(self.handle_update)
        self.line = None
        self.name = name
        self.plot_widget = plot_widget
        self.xdata = []
        self.ydata = []

    def make_line(self):
        line = matplotlib.lines.Line2D([], [])
        line.set_label(self.name)
        line.set_color(self.COLORS[self.plot_widget.next_color])
        self.plot_widget.next_color = (self.plot_widget.next_color + 1) % len(
            self.COLORS
        )
        self.axis.add_line(line)
        self.axis.legend(loc=self.axis.legend_loc)
        self.line = line

    def remove(self):
        self.line.remove()
        self.connection.remove()
        # NOTE jpieper: matplotlib gives us no better way to remove a
        # legend.
        if len(self.axis.lines) == 0:
            self.axis.legend_ = None
            self.axis.relim()
            self.axis.autoscale()
        else:
            self.axis.legend(loc=self.axis.legend_loc)
        self.plot_widget.canvas.draw()

    def handle_update(self, value):
        if self.plot_widget.paused:
            return

        if self.line is None:
            self.make_line()

        now = time.time()
        self.xdata.append(now)
        self.ydata.append(value)

        # Remove elements from the beginning until there is at most
        # one before the window.
        oldest_time = now - self.plot_widget.history_duration
        oldest_index = None
        for i in range(len(self.xdata)):
            if self.xdata[i] >= oldest_time:
                oldest_index = i - 1
                break

        if oldest_index and oldest_index > 1:
            self.xdata = self.xdata[oldest_index:]
            self.ydata = self.ydata[oldest_index:]

        self.line.set_data(self.xdata, self.ydata)
        self.axis.relim()
        self.axis.autoscale()
        self.plot_widget.data_update()
