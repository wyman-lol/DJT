$(function () {
    let $loginBtn = $('.loading');
    $loginBtn.click(function () {
        let telValue = $('input[name=telephone]').val();
        let pwdValue = $('input[name=password]').val();
        let $remember = $('input[name=remember]');
        //判断remember有没有钩上true或false
        let status_re = $remember.is(':checked');
        console.log(telValue,pwdValue);
        //    一般验证会做两次验证防止频繁请求
        if (telValue && pwdValue) {
            $.ajax({
            url:'/account/loading/',
            method:'post',
            data:{
                'telephone':telValue,
                'password':pwdValue,
                'remember':status_re,
            },
            dataType: "json",
            success: res=>{
                console.log(res);
                if(res["code"]===1){
                  message.showSuccess("登录成功");
                  setTimeout(()=>{
                      // 重定向当前页面url
                      window.location.href='/course/index/';
                      }, 1000
                  )

                }
                else{
                  message.showError(res["msg"])
                }
            },
            error: err=>{
                //当 ajax 出现问题的时候 返回
                logError(err);
            }
        });
        }
        else{
            message.showError('手机号码不能为空')
        }
    });
});
