$(function () {
  let $loginBtn = $(".login-btn");
  $loginBtn.click(function () {
    // 验证会做两层 前端防止频繁的发送请求
    let telVal = $("input[name=telephone]").val();
    let pwdVal = $("input[name=password]").val();
    let $remember = $("input[name=remember]");
    // console.log(`${telVal}, ${pwdVal}`)
    if (telVal && pwdVal) {
      // 获取 点击 单选框的状态  勾 true 没勾 false
    let status = $remember.is(":checked");
      let data = {
          "telephone": telVal,
          "password": pwdVal,
        };
      if(status){
        data["remember"] = status;
      }
      console.log(data);
      // 发送请求
      $.ajax({
        url: "/account/login/",
        method: "post",
        data: data,
        dataType: "json",
        success: res => {
          // console.log('success');
          console.log(res); // return JsonResponse 并不会展示在页面 通过ajax
          if (res["code"] === 2) {
            // 这里写成功之后执行代码   以后前端我全部写好 上课直接复制 后台代码慢慢讲
            message.showSuccess("登录成功");
            setTimeout(() => {
              window.location.href = '/';
            }, 2500);
          } else {
            message.showError(res["msg"]);
          }
        },
        error: err => {
          // // 当 ajax 出现问题的时候 返回
          // console.log('error');
          // console.log(err);
          logError(err);
        }
      })
    } else {
      message.showError("手机号和密码不能为空");
    }
  });

  let $graphCaptchaBtn = $(".form-item .captcha-graph-img");
  let $captchaImg = $graphCaptchaBtn.find('img');
  // 刷新图形验证码  没有必要太纠结
  $graphCaptchaBtn.click(function () {
    let oldSrc = $captchaImg.attr('src');
    console.log(oldSrc);
    // let newSrc = oldSrc.split("?")[0] + "?_=" + Date.now();
    // $captchaImg.attr('src', newSrc);
  });
});