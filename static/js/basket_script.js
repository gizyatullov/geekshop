'use strict';

window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        let t_href = event.target;

        $.ajax({
            url: `/basket/edit/${t_href.name}/${t_href.value}/`,

            success: function (data) {
                $('.basket_summary').html(data.basket_summary);
            },
        });

        event.preventDefault();
    });
}
