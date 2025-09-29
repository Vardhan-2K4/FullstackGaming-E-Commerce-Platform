(function($) {

    var $window = $(window),
        $body = $('body');

    // Breakpoints.
        breakpoints({
            xlarge:  [ '1281px',  '1680px' ],
            large:   [ '981px',   '1280px' ],
            medium:  [ '737px',   '980px'  ],
            small:   [ null,      '736px'  ]
        });

    // Play initial animations on page load.
        $window.on('load', function() {
            window.setTimeout(function() {
                $body.removeClass('is-preload');
            }, 100);
        });

    // Dropdowns.
        $('#nav > ul').dropotron({
            mode: 'fade',
            noOpenerFade: true,
            alignment: 'center'
        });

    // Nav.

    // Title Bar.
        $(
            '<div id="titleBar">' +
                '<a href="#navPanel" class="toggle"></a>' +
            '</div>'
        )
            .appendTo($body);

    // Panel.
        $(
            '<div id="navPanel">' +
                '<nav>' +
                    $('#nav').navList() +
                '</nav>' +
            '</div>'
        )
            .appendTo($body)
            .panel({
                delay: 500,
                hideOnClick: true,
                hideOnSwipe: true,
                resetScroll: true,
                resetForms: true,
                side: 'left',
                target: $body,
                visibleClass: 'navPanel-visible'
            });

    // --- FORM VALIDATION CODE ADDED FOR PROJECT ---
    // This code will run after the page is ready.
    $(document).ready(function() {
        // First, check if the contact form actually exists on the current page.
        if ($('#contact-form').length > 0) {
            $('#contact-form').on('submit', function(event) {
                $('#form-error').hide();

                const name = $('#name').val().trim();
                const email = $('#email').val().trim();
                const message = $('#message').val().trim();

                let isValid = true;

                if (name === '' || email === '' || message === '') {
                    isValid = false;
                }

                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(email)) {
                    isValid = false;
                }

                if (!isValid) {
                    $('#form-error').show();
                    event.preventDefault();
                }
            });
        }
    });

})(jQuery);