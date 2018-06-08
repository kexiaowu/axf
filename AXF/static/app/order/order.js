$(function () {

    //支付：需要集成第三方支付
    // 微信支付，支付宝，银联支付

    //点击支付
    $('#pay').click(function () {

        //支付完成后，需要讲订单状态更改
        $.get('/app/orderchangstatus/', {'orderid':$(this).attr('orderid'),'status':'1'},function (data) {
            // console.log(data)
            if (data.status == 1){
                location.href = '/app/mine/'
            }
            else {
                console.log(data.msg)
            }
        })
    })
});