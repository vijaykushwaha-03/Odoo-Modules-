/** @odoo-module **/

import { options } from "@web_editor/js/editor/snippets.options";

options.registry.AnnouncementBarOptions = options.Class.extend({
    init() {
        this._super(...arguments);
        this.setTarget(this.$target.closest('#wrapwrap > header'));
    },

    async _computeWidgetVisibility(widgetName, params) {
        switch (widgetName) {
            case 'announcement_bar_height': {
                return !!this.$('#announcement_bar').length;
            }
        }
        return this._super(...arguments);
    },
});
