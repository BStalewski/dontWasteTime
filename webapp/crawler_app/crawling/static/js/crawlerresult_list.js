var crawler = (function() {
    var that = {};

    that.accept = function(event) {
        update_status(event.target, '/crawling/accept/');
    };

    that.ignore = function(event) {
        update_status(event.target, '/crawling/ignore/');
    };

    function update_status(button, url_prefix) {
        var id = parseInt(button.id.split('-')[2]);
        var url = url_prefix + id + '/';
        $.post(url, {}, function() {
            var row = $('#result-' + id);
            row.remove();
        });
    }

    return that;
})();
