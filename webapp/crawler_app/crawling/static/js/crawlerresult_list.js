var crawler = (function() {
    var that = {};

    that.accept = function(event) {
        update_status(event.target, '/crawling/accept/');
    };

    that.ignore = function(event) {
        update_status(event.target, '/crawling/ignore/');
    };

    function update_status(target, url_prefix) {
        function find_button() {
            var element = $(target);
            while (element.prop('tagName') !== 'BUTTON') {
                element = element.parent();
            }
            return element;
        }

        var button = find_button();
        var id = parseInt(button.prop('id').split('-')[2]);
        var url = url_prefix + id + '/';
        $.post(url, {}, function() {
            var row = $('#result-' + id);
            row.remove();
        });
    }

    return that;
})();
