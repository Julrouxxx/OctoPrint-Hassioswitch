/*
 * View model for OctoPrint-Hassioswitch
 *
 * Author: Julien
 * License: AGPLv3
 */
$(function() {
    function HassioswitchViewModel(parameters) {
        const self = this;
        self.settings = parameters[0];

		self.toggle = function(){
		$.ajax({
			url: API_BASEURL + "plugin/hassioSwitch",
			type: "POST",
			dataType: "json",
			data: JSON.stringify({command: "toggle"}),
			contentType: "application/json; charset=UTF-8",
			success: function(d){
				if(d.result !== 200){
				new PNotify({title: 'HassioSwitch error',
							 text: 'Server issued error code: ' + d.result,
							 type: 'error',
							 hide: false})
				}
			}
		})
		};
        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: HassioswitchViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "settingsViewModel"/* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_hassioSwitch, #tab_plugin_hassioSwitch, ...
        elements: [ "#navbar_plugin_hassioSwitch"/* "#settings_plugin_hassioSwitch", "#navbar_plugin_hassioSwitch" ... */ ]
    });
});
