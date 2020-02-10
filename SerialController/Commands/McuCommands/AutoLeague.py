#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..McuCommandBase import McuCommand

# Mash A button
class AutoLeague(McuCommand):
	NAME = '自動リーグ周回'

	def __init__(self, sync_name = 'auto_league'):
		super().__init__(sync_name)
