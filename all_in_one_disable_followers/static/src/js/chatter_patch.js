import { patch } from "@web/core/utils/patch";
import { Chatter } from "@mail/chatter/web_portal/chatter";
import { useService } from "@web/core/utils/hooks";
import { onMounted, useEffect } from "@odoo/owl";

patch(Chatter.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        this.state.isFollowerDisabled = false;
        this.configSettingsDisableFollower = false;

        // runs only once after the component is mounted
        onMounted(async () => {
            try {
                const result = await this.orm.call(
                    "res.config.settings", "get_config_settings_followers", [], {}
                );

                this.configSettingsDisableFollower = result.configDisableFollower;

                // Initially set state based on both config and follower count
                const currentCount = this.state.thread?.followersCount ?? 0;
                this.state.isFollowerDisabled = this.configSettingsDisableFollower && currentCount === 0;
            } catch (error) {
                console.error("Follower config fetch error:", error);
            }
        });

        // runs on mount and when dependencies change
        useEffect(
            () => {
                const currentCount = this.state.thread?.followersCount ?? 0;
                // Only disable if config is true AND follower count is 0
                this.state.isFollowerDisabled = this.configSettingsDisableFollower && currentCount === 0;
            },
            () => [this.state.thread?.followersCount]
        );
    },

    get isDisabled() {
        return (
            !this.state.thread?.id ||
            !this.state.thread?.hasReadAccess ||
            this.state.isFollowerDisabled
        );
    },
});
