/*
 https://cloud.baidu.com/doc/MCT/WebSDKAPI.html#cyberplayer.3A.3Asetup
*/
let $videoUrl = $('.course-data').data('video-url');
let $cover = $('.course-data').data('cover-url');
let player = cyberplayer("course-video").setup({
    width: '100%', // 高度
    height: 720, // 宽度
    file: $videoUrl, // 地址
    image: $cover, //预览图
    autostart: false, // 自动播放
    stretching: "exactfit", // 缩放方式，缩放方式分为：1.none:不缩放；2.uniform:添加黑边缩放；3. exactfit:改变宽高比缩到最大；4.fill:剪切并缩放到最大（默认方式为uniform）
    repeat: false, // 重复播放
    volume: 77, // 音量
    controls: 'over', // 控制条显示
    tokenEncrypt: true,
    ak: '9ff8acf642b1463fa98245443227fb06', // AccessKey
});
player.on('beforePlay', (e) => {
    // 判断文件是否加密
    if (!/m3u8/.test(e.file)) {
        return false;
    }
    $.get({
        "url": "/course/token/",
        "data": {
            "video_url": videoUrl,
        },
        "success": res => {
            let token = res['token'];
            player.setToken(e.file, token)
        },
        "error": err => {
            console.log(err);
            console.log(err.status + "====" + err.statusText);

        }
    });
});