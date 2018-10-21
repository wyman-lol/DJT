$(function () {
    // 图片验证码
    // 获取img标签
    let $graphCaptchaBtn = $(".png");
    // 利用url的时间戳刷新图形验证码
    $graphCaptchaBtn.click(function () {
    // 获取img标签的src地址
    let oldSrc = $graphCaptchaBtn.attr('src');
    // 拼接src加上时间戳
    let newSrc = oldSrc.split("?")[0] + "?_=" + Date.now();
    $graphCaptchaBtn.attr('src', newSrc);
  });

    // 发送手机验证码
    // 获取元素
    let $smsCaptchaBtn = $(".send");
    let $telephone = $(".telephone");
    let reg = /^((1[3-9][0-9])+\d{8})$/; // 判断手机号
    // 发送短信验证码
    $smsCaptchaBtn.click(function () {
    message.showInfo("验证码已经发送，请注意查收");
    let telVal = $telephone.val();
    // trim()两端去空格 test()方法用于检测一个字符串是否匹配某个模式.
    if (telVal && telVal.trim()) {
      if (reg.test(telVal)) {
        $.ajax({
          url: "/account/sms_send/",
          method: "get",
          data: {
            "telphone": telVal,
          },
          success: res => {
            console.log(res);
            console.log(typeof res);
            // 控制几秒后重发
            let count = 60;
            // text() 方法方法设置或返回被选元素的文本内容。
            // let $text = $(this).text();
            let $text = $(this).val();
            $(this).attr('disabled', true);
            let timer = setInterval(() => {
              $(this).val(count+'秒后再次发送');
              count--;
              if (count <= 0) {
                clearInterval(timer);
                $(this).val($text);
                $(this).removeAttr('disabled');
              }
            }, 1000);
          },
          error: err => {
            logError(err);
          }
        })
      }
      else {
        message.showError('手机号格式不正确');
        // 当元素获得焦点时，发生 focus 事件。
        $telephone.focus();
      }
    }
    else {
      message.showError('请输入手机号');
      $telephone.focus();
    }
    });
    // 注册
      // 注册按钮
      let $regBtn = $(".register");
      // 获取元素
      let $smsCaptcha = $(".sms_captcha");
      let $username = $(".username");
      let $password = $(".password");
      let $passwordRepeat = $(".repeat_password");
      let $graphCaptcha = $(".graph_captcha");
      $regBtn.click(function (ev) {
        ev.preventDefault()
        // 获取值
        let telVal = $telephone.val();
        let smsCaptchaVal = $smsCaptcha.val();
        let userVal = $username.val();
        let pwdVal = $password.val();
        let pwdRepeatVal = $passwordRepeat.val();
        let graphCaptchaVal = $graphCaptcha.val();
         $.ajax({
            url: "/account/register/",
            method:"post",
            data: {
                "telephone": telVal,
                "sms_captcha": smsCaptchaVal,
                "username": userVal,
                "password": pwdVal,
                "repeat_password": pwdRepeatVal,
                "graph_captcha": graphCaptchaVal,
          },
            success: res => {
                if (res["code"] === 2) {
                  window.message.showSuccess("注册成功");
                  setTimeout(() => {
                    window.location.href = '/course/index/';
                  }, 1000)
                } else {
                      window.message.showError(res["msg"])
                    }
            },
            error: err => {
                logError(err)
            }
            })
      });
});
