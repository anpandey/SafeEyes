# Safe Eyes is a utility to remind you to take break frequently
# to protect your eyes from eye strain.

# Copyright (C) 2017  Gobinath

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

import gi

from safeeyes.context import Context
from safeeyes.spi.breaks import BreakType, Break
from safeeyes.util.locale import _

gi.require_version("Notify", "0.7")
from gi.repository import Notify

"""
Safe Eyes Notification plugin
"""

APPINDICATOR_ID = "safeeyes"
notification = None
context = None
warning_time = 10

Notify.init(APPINDICATOR_ID)


def init(ctx: Context, plugin_config: dict) -> None:
    """
    Initialize the plugin.
    """
    global context
    global warning_time
    context = ctx
    warning_time = ctx.config.get("pre_break_warning_time")


def on_pre_break(break_obj: Break) -> None:
    """
    Show the notification
    """
    # Construct the message based on the type of the next break
    global notification
    logging.debug("Notification: show the notification")
    message = "\n"
    if break_obj.type == BreakType.SHORT:
        message += (_("Ready for a short break in %s seconds") % warning_time)
    else:
        message += (_("Ready for a long break in %s seconds") % warning_time)

    notification = Notify.Notification.new("Safe Eyes", message, icon="safeeyes_enabled")
    try:
        notification.show()
    except BaseException:
        logging.error("Notification: failed to show the notification")


def on_start_break(break_obj: Break) -> None:
    """
    Close the notification.
    """
    global notification
    if notification:
        try:
            notification.close()
            notification = None
        except BaseException:
            # Some operating systems automatically close the notification.
            pass


def on_exit() -> None:
    """
    Uninitialize the registered notificaion.
    """
    logging.info("Notification: stop the plugin")
    Notify.uninit()
