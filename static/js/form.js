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


