window.onload = function () {
    var _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    var quantity_arr = [];
    var price_arr = [];

    var TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    var order_get_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    var order_get_total_price = parseFloat($('.order_get_total_price').text().replace(',', '.')) || 0;

    for (var i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }

    if (!order_get_total_quantity) {
        for (var i = 0; i < TOTAL_FORMS; i++) {
            order_get_total_quantity += quantity_arr[i];
            order_get_total_price += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_get_total_quantity.toString());
        $('.order_get_total_price').html(Number(order_get_total_price.toFixed(2)).toString());
    }

    $('.order_form').on('click', 'input[type="number"]', function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
    });

    function deleteOrderItem(row) {
        var target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }

    $('.order_form select').change(function () {
        var target = event.target;
        console.log(target);
    });

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;

        order_get_total_price = Number((order_get_total_price + delta_cost).toFixed(2));
        order_get_total_quantity = order_get_total_quantity + delta_quantity;

        $('.order_get_total_price').html(order_get_total_price.toString());
        $('.order_total_quantity').html(order_get_total_quantity.toString());
    }

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });
}