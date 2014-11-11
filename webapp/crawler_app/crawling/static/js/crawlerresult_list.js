var crawler = (function() {
    var that = {};

    that.accept = function(event) {
        update_status(event, '/crawling/accept/');
    };

    that.ignore = function(event) {
        update_status(event, '/crawling/ignore/');
    };

    function update_status(event, url_prefix) {
        function find_button(event) {
            var element;
            for (var i = 0; i < event.path.length; i += 1) {
                element = $(event.path[i]);
                if (element.prop('tagName') === 'BUTTON') {
                    return element;
                }
            }
        }

        var button = find_button(event);
        var id = parseInt(button.prop('id').split('-')[2]);
        var url = url_prefix + id + '/';
        $.post(url, {}, function() {
            var row = $('#result-' + id);
            row.remove();
        });
    }

    return that;
})();
