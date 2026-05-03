(function () {
    'use strict';

    var cachedContext = { suite_id: '', test_id: '', kw_name: '', ts: '' };

    function ts() {
        return new Date().toISOString();
    }

    function targetDescription(target) {
        if (!target || !target.tagName) {
            return null;
        }
        return target.id ? '#' + target.id : target.tagName.toLowerCase();
    }

    function refreshContext() {
        fetch('/rf-context', { keepalive: true })
            .then(function (r) {
                return r.json();
            })
            .then(function (ctx) {
                cachedContext = ctx || cachedContext;
            })
            .catch(function () {});
    }

    function sendEvent(event_type, extra) {
        var payload = Object.assign(
            { ts: ts(), event_type: event_type, url: location.href, rf_context: cachedContext },
            extra,
        );
        fetch('/browser-events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            keepalive: true,
        }).catch(function () {});

        // Keep context fresh asynchronously; do not block event delivery on this roundtrip.
        refreshContext();
    }

    // Prime context once on load.
    refreshContext();

    // Clicks (capture phase so we see all clicks before handlers suppress them)
    document.addEventListener(
        'click',
        function (e) {
            sendEvent('click', { target: targetDescription(e.target) });
        },
        true,
    );

    // Pointer and mouse interactions used by drag/drop style tests.
    function attachInteractionListener(type) {
        document.addEventListener(
            type,
            function (e) {
                sendEvent(type, {
                    target: targetDescription(e.target),
                    x: typeof e.clientX === 'number' ? e.clientX : null,
                    y: typeof e.clientY === 'number' ? e.clientY : null,
                    button: typeof e.button === 'number' ? e.button : null,
                    buttons: typeof e.buttons === 'number' ? e.buttons : null,
                });
            },
            true,
        );
    }

    ['pointerdown', 'pointerup', 'mousedown', 'mouseup', 'dragstart', 'drop'].forEach(attachInteractionListener);

    // Form submits
    document.addEventListener(
        'submit',
        function (e) {
            sendEvent('submit', {
                target: targetDescription(e.target),
                action: e.target ? e.target.action : null,
            });
        },
        true,
    );

    // Console errors
    var _origConsoleError = console.error;
    console.error = function () {
        var args = Array.prototype.slice.call(arguments);
        sendEvent('console_error', { message: args.map(String).join(' ') });
        return _origConsoleError.apply(console, args);
    };

    // Uncaught JS errors
    window.addEventListener('error', function (e) {
        sendEvent('page_error', {
            message: e.message,
            source: e.filename + ':' + e.lineno,
        });
    });

    // Unhandled promise rejections
    window.addEventListener('unhandledrejection', function (e) {
        sendEvent('unhandledrejection', { message: String(e.reason) });
    });

    // Navigation signals
    window.addEventListener('beforeunload', function () {
        sendEvent('navigation', { to: null, trigger: 'beforeunload' });
    });

    window.addEventListener('popstate', function () {
        sendEvent('navigation', { to: location.href, trigger: 'popstate' });
    });

    window.addEventListener('hashchange', function (e) {
        sendEvent('navigation', { to: e.newURL, trigger: 'hashchange' });
    });
})();
