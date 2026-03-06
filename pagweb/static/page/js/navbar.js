(function () {
    'use strict';

    const navbar     = document.getElementById('navbar');
    const menuToggle = document.getElementById('menuToggle');
    const navMenu    = document.getElementById('navMenu');

    if (!navbar || !menuToggle || !navMenu) return;

    let lastScroll = 0;
    window.addEventListener('scroll', function () {
        const current = window.pageYOffset;
        if (current > 80) {
            navbar.classList.toggle('nav-hidden', current > lastScroll);
            navbar.classList.add('nav-scrolled');
        } else {
            navbar.classList.remove('nav-hidden', 'nav-scrolled');
        }
        lastScroll = current;
    }, { passive: true });

    menuToggle.addEventListener('click', function () {
        menuToggle.classList.toggle('is-active');
        navMenu.classList.toggle('menu-open');
    });

    navMenu.querySelectorAll('.nav-link').forEach(function (link) {
        link.addEventListener('click', function () {
            menuToggle.classList.remove('is-active');
            navMenu.classList.remove('menu-open');
        });
    });

    document.addEventListener('click', function (e) {
        if (!navbar.contains(e.target)) {
            menuToggle.classList.remove('is-active');
            navMenu.classList.remove('menu-open');
        }
    });
})();