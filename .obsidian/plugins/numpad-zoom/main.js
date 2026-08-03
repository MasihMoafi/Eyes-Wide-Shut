const { Plugin } = require("obsidian");

module.exports = class NumpadZoomPlugin extends Plugin {
	onload() {
		this.registerDomEvent(window, "keydown", (event) => {
			if (
				!event.ctrlKey ||
				event.shiftKey ||
				event.altKey ||
				event.metaKey
			) {
				return;
			}

			if (event.code === "NumpadAdd") {
				event.preventDefault();
				event.stopImmediatePropagation();
				this.app.commands.executeCommandById("window:zoom-in");
			} else if (event.code === "NumpadSubtract") {
				event.preventDefault();
				event.stopImmediatePropagation();
				this.app.commands.executeCommandById("window:zoom-out");
			}
		}, true);
	}
};
