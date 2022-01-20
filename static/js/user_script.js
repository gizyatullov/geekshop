'use strict';

window.onload = function () {
    $('.users_list').on('click', 'input[type="button"]', function () {
        let t_href = event.target;

        $.ajax({
            url: `/admin/users/delete/${t_href.name}/`,

            success: function (data) {
                $('.users_list').html(`${data.correction}`);
            },
        });

        event.preventDefault();
    });
}
