# coding=utf-8
from __future__ import absolute_import

# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.
import octoprint.plugin
import threading


class HassioswitchPlugin(octoprint.plugin.SettingsPlugin, octoprint.plugin.AssetPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.SimpleApiPlugin, octoprint.plugin.EventHandlerPlugin):

	# ~~ SettingsPlugin mixins
	def get_settings_defaults(self):
		return dict(
			url="https://192.168.1.20:8123",
			auth_token="",
			entity_name="switch.printer",
			auto_connect=True
		)

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=True),
			dict(type="settings", custom_bindings=False)
		]

	# #~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/hassioSwitch.js"]
		)

	# #~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			hassioSwitch=dict(
				displayName="Hassioswitch Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="Julrouxxx",
				repo="OctoPrint-Hassioswitch",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/Julrouxxx/OctoPrint-Hassioswitch/archive/{target_version}.zip"
			)
		)

	def toggledevices(self):
		import requests
		import flask
		if not self._printer.is_closed_or_error() and (self._printer.is_printing() or self._printer.is_paused()):
			return flask.jsonify(result=0)

		ip = self._settings.get(['url']) + "api/services/switch/toggle"
		auth_token = self._settings.get(['auth_token'])
		switch = self._settings.get(['entity_name'])
		payload = {'entity_id': switch}
		headers = {
			'Authorization': 'Bearer ' + auth_token
		}

		x = requests.post(ip, headers=headers, json=payload)
		if x.status_code == 200:
			state = x.json()[0]['state']
			if state == 'on':
				if self._settings.get(['auto_connect']):
					threading.Timer(10, self._printer.connect).start()
			else:
				self._printer.disconnect()

		return flask.jsonify(result=x.status_code)

	def get_api_commands(self):
		return dict(toggle=[])

	def on_api_command(self, command, data):
		import flask
		if command == "toggle":
			r = self.toggledevices()
			return r


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "HassioSwitch"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
# __plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4"  # python 2 and 3


def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = HassioswitchPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
