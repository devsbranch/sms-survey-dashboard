/*! dashboard.js | Bulkit | CSS Ninja */

/* ==========================================================================
Dashboard core JS file
========================================================================== */

//Init demo search
function initSearch() {
    $('.search-field').on('keyup', function () {
        var $this = $(this);
        var $container = $this.closest('.control');
        var searchQuery = $this.val();
        var expression = new RegExp(searchQuery, "i");
        $.getJSON('assets/data/search.json', function (data) {
            $container.find('.search-results .search-result, .search-results .placeholder-wrap').remove();
            $.each(data, function (key, value) {
                if (value.title.search(expression) != -1 || value.content.search(expression) != -1) {

                    if (value.photoUrl === null) {
                        var template = `
                            <a class="search-result">
                                <div class="fake-avatar" style="background:${value.color}">
                                    <span>${value.title.slice(0, 1)}</span>
                                </div>
                                <div class="meta">
                                    <span>${value.title}</span>
                                    <span>${value.content}</span>
                                </div>
                            </a>
                        `
                    }

                    else {
                        var template = `
                            <a class="search-result">
                                <img class="${value.type === 'user' ? 'avatar' : 'record'}" src="${value.photoUrl}" alt="">
                                <div class="meta">
                                    <span>${value.title}</span>
                                    <span>${value.content}</span>
                                </div>
                            </a>
                        `
                    }

                    $container.find('.search-results').append(template);
                }
            })

            if ($container.find('.search-result').length === 0) {
                var placeholder = `
                        <div class="placeholder-wrap">
                            <div class="placeholder-content has-text-centered">
                                <img src="assets/images/illustrations/no-results.svg" alt="">
                                <h3>No Matching Results</h3>
                                <p>Sorry, we couldn't find any matching records. Please try different search terms.</p>
                            </div>
                        </div>
                    `

                $container.find('.search-results').append(placeholder);
            }
        })

        if (searchQuery === '') {
            $container.find('.search-results').removeClass('is-active');
        } else {
            $container.find('.search-results').addClass('is-active');
        }
    })
}

$(document).ready(function($){

    "use strict";

    //Change demo images
    $('*[data-demo-src]').each(function () {
        var newSrc = $(this).attr('data-demo-src');
        if (newSrc !== undefined) {
            $(this).attr('src', newSrc);
        }
    });

    feather.replace();

    initSearch();

    //Auto set mobile layout to reader mode on page load
    setTimeout(function(){
        if (window.matchMedia('(max-width: 767px)').matches) {
            $('#reader-mode-toggle').trigger('click');
            $('#reader-mode-switch').trigger('change');
        }
    }, 500);

    //Mobile menu toggle
    $().initMobileMenu();

    $().initDashboardLayout();

    //Attribute background images
    $().initBgImages();

    //Pop Dropdowns
    $().initPopDropdowns();

    //Common dropdown
    $().initDropdowns();

    //Init Modals
    $().initModals();

    //Init Alert boxes
    $().initAlertBoxes();

    //Navigation Tabs
    $().initNavigationTabs();

    //Ripple effect
    $().initRipple();

    //Custom quickview initialization with data attributes
    $().initQuickview();

    //datepicker initialization
    $().initDatepicker();

    //wickedpicker 24 hours initialization
    $().initTimepicker();

    //Accordion initialization
    $().initAccordion();

    //Chosen select initialization
    $().initChosenSelect();

    //Adding the styled checkbox styles
    $().initCheckboxes();

    //Initialize tooltips
    $().initTooltips();

    //Initialize popovers
    $().initPopovers();

    //Busy switch behaviour
    $().initBusySwitch();

    //Complete task fab button
    $().initTaskFab();

    //Social Fab menu
    $().initSocialFab();

    //Like button
    $().initLikeButton();

    //Init Profile section
    $().initProfile();

    //Fake chat messages simulation
    $().initChat();

    //Media card background images
    $().initMediaCards();

    //Svg vector map
    $().initVectorMap();

})

