$(function () {

    flag1 = false;  //表示用户名输入是否合法
    flag2 = false;  // 密码
    flag3 = false;  // 确认密码
    flag4 = false;  // 邮箱

    //用户名
    // $('#username').change(function () {
    //     // console.log($(this).val());
    //     var value = $(this).val();
    //     if (/^[a-zA-Z_]\w{5,17}$/.test(value)){
    //
    //         // console.log('输入合法');
    //         flag1 = true;
    //     }
    //     else {
    //         // console.log('输入有误');
    //         flag1 = false;
    //     }
    //
    // });

    //用户名
    $('#username').change(function () {
        var v = $(this).val();
        if (/^[a-zA-Z_]\w{5,17}$/.test(v)){

            flag1 = true;

            //如果输入格式正确，则验证用户名是否存在
            $.get('/app/checkusername/',{username: $(this).val()}, function (data) {
            // console.log(data)
                if (data.status == 1) {
                    $('#msg').html('用户名可以使用').css('color', 'green')
                }
                else if (data['status'] == 0) {
                    $('#msg').html(data.msg).css('color', 'red')
                }
                else  {
                    $('#msg').html('用户名不合法').css('color', 'green')

                }
            })

        }
        else {
            flag1 = false;
            $('#msg').html('用户名输入有误').css('color', 'orange')

        }

    });

     //密码
    $('#password').change(function () {
        // console.log($(this).val());
        var v = $(this).val();
        if (/^.{8,}$/.test(v)){

            // console.log('输入合法');
            flag2 = true;
        }
        else {
            // console.log('输入有误');
            flag2 =false;
        }

    });

      //确认密码
    $('#again').change(function () {
        // console.log($(this).val());
        if ($(this).val() == $ ('#password').val()){

            // console.log('输入合法');
            flag3 = true;
        }
        else {
            // console.log('输入有误');
            flag3 = false;
        }

    });

      //邮箱
    $('#email').change(function () {
        // console.log($(this).val());
        var value = $(this).val();
        if (/^\w+@\w+\.\w+$/.test(value)){

            // console.log('输入合法');
            flag4 = true;
        }
        else {
            // console.log('输入有误');
            flag4 = false
        }

    });

    //注册
    $('#register').click(function(){

        if (flag1 && flag2 && flag3 && flag4){

            //表单提交md5加密后的密码
            $('#password').val(md5($('#password').val()));
            return true
        }
        else{
            alert('输入有误');
            return false
        }


    });

    //检测用户名是否存在
    $('#username').change(function () {

        /*
        $.ajax({
            'type': 'get',  //默认get，可以不写
            url: '', //路径，必须写
            data: {},  //参数
            async: true,  //可以不写，默认时true

            //请求成功的回调函数
            success: function (data) {
                console.log(data)

            },

            //请求失败的回调函数
            error: function (err) {
                console.log(err)
            }
        });
        */

        /*
        $.get('url',{}, function (data) {

        })
        */

        /*
        $.post('url',{}, function (data) {

        })
        */

        /*
        $.getJSON('url',{}, function () {

        })
        */

        /*
        var xhr = XMLHttpRequest();
        xhr.open('get', 'url', true);
        xhr.send();
        xhr.onreadystatechange = function () {
            if (xhr.readyState ==4 && xhr.status == 200){
                console.log(xhr.responseText)
            }
        }
        */


        // $.get('app/checkusername/',{username: $(this).val()}, function (data) {
        //     // console.log(data)
        //     if (data.status == 1) {
        //         $('#msg').html('用户名可以使用').css('color', 'green')
        //     }
        //     else if (data['status'] == 0) {
        //         $('#msg').html(data.msg).css('color', 'red')
        //     }
        //     else {
        //         $('#msg').html('用户名不合法').css('color', 'green')
        //
        //     }
        // })
    });




});