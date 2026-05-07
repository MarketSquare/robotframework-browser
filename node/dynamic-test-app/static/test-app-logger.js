(function () {
    'use strict';

    function post(payload) {
        var data = JSON.stringify(Object.assign({ url: location.href }, payload));
        if (navigator.sendBeacon) {
            navigator.sendBeacon('/api/log/event', new Blob([data], { type: 'application/json' }));
        } else {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/api/log/event', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(data);
        }
    }

    function label(el) {
        return (el.getAttribute('aria-label') || el.textContent || el.value || el.id || el.name || '')
            .trim()
            .slice(0, 80);
    }

    document.addEventListener(
        'click',
        function (e) {
            var el = e.target;
            var tag = el.tagName ? el.tagName.toLowerCase() : '';
            if (['button', 'a', 'input', 'label'].indexOf(tag) !== -1 || el.closest('button,a')) {
                post({ event: 'click', tag: tag, text: label(el) });
            }
        },
        true,
    );

    document.addEventListener(
        'change',
        function (e) {
            var el = e.target;
            var tag = el.tagName ? el.tagName.toLowerCase() : '';
            var type = (el.type || '').toLowerCase();
            if (tag === 'select' || type === 'checkbox' || type === 'radio') {
                post({ event: 'change', tag: tag, type: type, text: label(el), value: el.value });
            }
        },
        true,
    );

    document.addEventListener(
        'submit',
        function (e) {
            var el = e.target;
            post({ event: 'submit', tag: 'form', id: el.id || '', action: el.action || '' });
        },
        true,
    );

    document.addEventListener(
        'dragstart',
        function (e) {
            var el = e.target;
            post({ event: 'dragstart', tag: el.tagName ? el.tagName.toLowerCase() : '', text: label(el) });
        },
        true,
    );

    document.addEventListener(
        'drop',
        function (e) {
            var el = e.target;
            post({ event: 'drop', tag: el.tagName ? el.tagName.toLowerCase() : '', text: label(el) });
        },
        true,
    );

    document.addEventListener(
        'mouseenter',
        function (e) {
            var el = e.target;
            var tag = el.tagName ? el.tagName.toLowerCase() : '';
            if (['button', 'a', 'input', 'select'].indexOf(tag) !== -1) {
                post({ event: 'hover', tag: tag, text: label(el) });
            }
        },
        true,
    );

    window.addEventListener('load', function () {
        post({ event: 'load', title: document.title });
    });

    window.addEventListener('popstate', function () {
        post({ event: 'popstate', title: document.title });
    });
})();
