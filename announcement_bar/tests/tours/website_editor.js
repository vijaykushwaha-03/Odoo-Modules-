registerWebsitePreviewTour('website_announcement_bar_test', {
    url: '/',
    edition: true,
}, () => [
    {
        content: "Click the logo or announcement bar",
        trigger: ':iframe #announcement_bar',
        run: "click",
    },
]);
