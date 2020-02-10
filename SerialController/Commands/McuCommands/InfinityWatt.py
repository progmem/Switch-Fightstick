#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..McuCommandBase import McuCommand

# Mash A button
class InfinityWatt(McuCommand):
	NAME = '無限ワット'

	def __init__(self, sync_name = 'inf_watt'):
		super().__init__(sync_name)
