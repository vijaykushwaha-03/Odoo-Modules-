import { patch } from "@web/core/utils/patch";
import { SaverScreen } from "@point_of_sale/app/screens/saver_screen/saver_screen";

patch(SaverScreen.prototype, {
    // Extend the existing component with new props
    setup() {
        super.setup?.();
        this.config = this.props.config;
    },
});

SaverScreen.props = {
    ...SaverScreen.props,
    config: Object,
};
