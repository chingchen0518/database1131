// student_detail.js

document.addEventListener('DOMContentLoaded', function() {
    var acc = document.querySelectorAll(".accordion-button");

    acc.forEach(function(button) {
        button.addEventListener("click", function() {
            var input = button.previousElementSibling;
            var arrow = button.querySelector(".arrow");

            if (input.checked) {
                button.classList.remove("active");
                arrow.innerHTML = "&#x25B6;"; // right arrow
            } else {
                button.classList.add("active");
                arrow.innerHTML = "&#9660;"; // Up arrow
            }
        });
    });
});
