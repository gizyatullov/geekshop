'use strict';

window.onload = function () {
    $('.categories_list').on('click', 'input[type="button"]', function () {
        let t_href = event.target;

        $.ajax({
            url: `/admin/categories/delete/${t_href.name}/`,

            success: function (data) {
                $('.categories_list').html(`${data.correction}`);
            },
        });

        event.preventDefault();
    });
}
