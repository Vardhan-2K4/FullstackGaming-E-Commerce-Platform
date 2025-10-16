# Frontend Components and Client Behavior

The project uses server-rendered templates (Jinja2) with light JavaScript.

## Forms
- Contact form (`#contactForm`): validated client-side by `static/js/form.js`

### static/js/form.js
```javascript
$(function () {
  $("#contactForm").on("submit", function (e) {
    var name = $("#name").val().trim();
    var email = $("#email").val().trim();
    var message = $("#message").val().trim();
    if (!name || !email || !message) {
      e.preventDefault();
      $("#clientSuccess").addClass("d-none");
      alert("Please fill out all fields.");
      return;
    }
    $("#clientSuccess").removeClass("d-none");
  });
});
```

## Templates
Key templates rendered by routes:
- `templates/index.html`
- `templates/login.html`
- `templates/register.html`
- `templates/profile.html`
- `templates/cart.html`
- `templates/checkout.html`
- Content pages: `bgmi.html`, `freefire.html`, `gta5.html`, `mw2.html`, `valorant.html`, `triology.html`, `playstation.html`, `nintendo.html`, `origin.html`

## Static Assets
- `assets/js/*.js`: third-party helpers (breakpoints, browser, jQuery plugins)
- `static/css/custom.css`: project-specific styles
