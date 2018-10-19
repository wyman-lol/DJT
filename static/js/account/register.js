$(function () {
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
});
