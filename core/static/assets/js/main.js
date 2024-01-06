

(function () {
    //===== Prealoder

    window.onload = function () {
        window.setTimeout(fadeout, 500);
    }

    function fadeout() {
        document.querySelector('.preloader').style.opacity = '0';
        document.querySelector('.preloader').style.display = 'none';
    }


    /*=====================================
    Sticky
    ======================================= */
    /*=====================================
Sticky
======================================= */
window.onscroll = function () {
    var header_navbar = document.querySelector(".navbar-area");
    var sticky = header_navbar.offsetTop;

    // show or hide the back-top-top button
    var backToTo = document.querySelector(".scroll-top");
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
        backToTo.style.display = "flex";
    } else {
        backToTo.style.display = "none";
    }
};

// Function to handle the "Back to Top" button click
function redirectTo404() {
    // Redirect to the 404.html page
    window.location.href = "404.html";
}

// Attach the function to the "Back to Top" button click event
var backToTopButton = document.querySelector(".scroll-top");
backToTopButton.addEventListener('click', redirectTo404);

//===== mobile-menu-btn
let navbarToggler = document.querySelector(".mobile-menu-btn");
navbarToggler.addEventListener('click', function () {
    navbarToggler.classList.toggle("active");
});



})();
