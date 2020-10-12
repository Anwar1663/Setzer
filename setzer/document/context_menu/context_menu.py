#!/usr/bin/env python3
# coding: utf-8

# Copyright (C) 2017, 2018 Robert Griesel
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import setzer.document.context_menu.context_menu_controller as context_menu_controller
import setzer.document.context_menu.context_menu_presenter as context_menu_presenter
import setzer.document.context_menu.context_menu_viewgtk as context_menu_view


class ContextMenu(object):
    
    def __init__(self, document, document_view):
        self.document = document
        self.document_view = document_view
        self.scbar_view = context_menu_view.ContextMenuView(document)
        stack = document_view.shortcuts_bar_bottom.more_actions_popover.get_child()
        stack.add_named(self.scbar_view, 'main')
        self.controller = context_menu_controller.ContextMenuController(self, self.scbar_view)
        self.presenter = context_menu_presenter.ContextMenuPresenter(self, self.scbar_view)

        document.register_observer(self)

    def change_notification(self, change_code, notifying_object, parameter):

        if change_code == 'can_forward_sync_changed':
            self.presenter.on_can_forward_sync_changed(parameter)
            
    def on_undo(self, widget=None):
        self.document_view.source_view.emit('undo')

    def on_redo(self, widget=None):
        self.document_view.source_view.emit('redo')

    def on_cut(self, widget=None):
        self.document_view.source_view.emit('cut-clipboard')

    def on_copy(self, widget=None):
        self.document_view.source_view.emit('copy-clipboard')

    def on_paste(self, widget=None):
        self.document_view.source_view.emit('paste-clipboard')

    def on_delete(self, widget=None):
        self.document_view.source_view.emit('delete-from-cursor', Gtk.DeleteType.CHARS, 0)

    def on_select_all(self, widget=None):
        self.document_view.source_view.emit('select-all', True)

    def on_show_in_preview(self, widget=None):
        self.document.forward_sync()

    def on_toggle_comment(self, menu_item):
        self.document.comment_uncomment()


