# HUD


# TODO write Hud.notification() and add support for automatic line wrapping


try:
	import sys
	import pygame
	import pygame.font

	from constants import (
		TILE_SIZE,
		HUD_MARGIN,
		VIEWPORT_WIDTH, VIEWPORT_HEIGHT
	)
	from utils import load_scaled_image
except ImportError as importErr:
	print("Couldn't load module. {}".format(importErr))
	sys.exit(2)


# -------------------------------------------------------------------------------------------------


class Hud(object):
	"""UI rendering class
	Returns: object
	Attributes:
		font_name (str)
		size (int)
		bold (bool)
		italic (bool)
		antialias (bool)
		color (rgb tuple)"""
	def __init__(
		self,
		surface,
		font_name=None, hud_size=32,
		bold=False, italic=False, antialias=True,
		color=(255, 255, 255)
	):
		# Initialize the font module if needed
		if not pygame.font.get_init(): pygame.font.init()
		# Surface used for rendering
		self.surface = surface
		# Font name, will try a similar alternative or fallback to pygame font
		self.font_name = font_name
		# General text size
		self.size = hud_size
		# Use antialias when rendering text
		self.antialias = antialias
		# Default color to use
		self.color = color
		# Default line height (in pixels)
		self._line_height = 3
		# Default icons size
		self._icons_size = (24, 24)
		# HUD icons by tag
		self._icons = {
			"default": 	load_scaled_image("unknown.png", self._icons_size),
			"life": 	load_scaled_image("heart.png", self._icons_size),
			"damage": 	load_scaled_image("weap_hand_L.png", self._icons_size),
			"shield": 	load_scaled_image("defense_placeholder.png", self._icons_size),
			"movement": load_scaled_image("speed_placeholder.png", self._icons_size),
		}
		# Create font object
		self.font = pygame.font.SysFont(font_name, hud_size, bold=bold, italic=italic)

	def _render_text(self, text, x, y, surface=None, color=None):
		"""Generic rendering method: draws a text on a surface at the given coordinates"""
		# Use internal surface when none is available in the arguments
		if not surface: surface = self.surface
		# Render text to font surface
		text_surface = self.font.render(text, self.antialias, color if color else self.color)
		# Draw text on surface
		surface.blit(text_surface, (x, y))

	def _render_surface(self, source_surface, x, y, surface=None):
		"""Generic rendering method: draws a pygame.Surface on another surface at the given coordinates"""
		# Use internal surface when none is available in the arguments
		if not surface: surface = self.surface
		# Draw text on surface
		surface.blit(source_surface, (x, y))

	def _render_player_life(self, value, max_value):
		"""Internal, renders the top-left section of the HUD: player life"""
		text = "HP {}/{}".format(value, max_value)
		self._render_text(text, HUD_MARGIN, HUD_MARGIN)

	def _render_kill_counter(self, kill_count):
		"""Internal, renders the top-right section of the HUD: kill counter (score)"""
		text = "{} Kills".format(kill_count)
		text_margin_right = self.font.size(text)[0] + HUD_MARGIN
		self._render_text(text, VIEWPORT_WIDTH - text_margin_right, HUD_MARGIN)

	def _render_player_stats(self, stats):
		"""Internal, renders the bottom-left section of the HUD: player stats and bonuses"""
		# Number of stats that still need to be rendered
		remaining_lines = len(stats.keys())
		# Starting position for each line
		line_pos_x = HUD_MARGIN
		line_pos_y = 0
		# Starting position for text (next to the icon)
		text_pos_x = self._icons_size[0] + line_pos_x
		# Line size on the y axis (line max height + spacing height)
		line_size_y = max(self._icons_size[1], self.font.size("00 ")[1]) + self._line_height
		# Render stats in lines, in the bottom left section of the HUD
		text = ""
		icon = None
		for key in stats.keys():
			# Build formatted string for current line
			text = "{}".format(stats[key]["base"])
			# Add bonus where needed
			if stats[key]["bonus"] != 0:
				text = "{} +{}".format(text, stats[key]["bonus"])
			# Assign icon by category
			icon = self._icons[key] if key in self._icons else self._icons["default"]
			# Update vertical position
			line_pos_y = VIEWPORT_HEIGHT - remaining_lines * line_size_y - HUD_MARGIN
			# Render icon + text
			self._render_surface(icon, line_pos_x, line_pos_y)
			self._render_text(text, text_pos_x, line_pos_y)
			# Update line counter
			remaining_lines -= 1

	def render_hud(self, player_stats, kill_count):
		"""Renders the whole game HUD: life, score and player stats"""
		# Top Left
		self._render_player_life(	player_stats["life"]["current"],								# HP
									player_stats["life"]["base"] + player_stats["life"]["bonus"]) 	# Max HP
		# Top Right
		self._render_kill_counter(kill_count)
		# Bottom Right
		self._render_player_stats(player_stats)

	def notification(self, text, cooldown=3, color=None):
		"""TODO docstring for Hud.notification()"""
		pass
