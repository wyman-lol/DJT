$(function () {
    var $img = $('.banner .photo img');
    var $btn = $('.banner .btn li');
    var $select = $('.banner .select li');
    var $banner = $('.banner')
    var index = 0;
    var len = $select.length;
    //初始化第一张图片
    $img.eq(0).addClass('show');
    $select.eq(0).addClass('activate');

    //改变图片函数
    function change($obj1, $obj2, num) {
        $obj1.eq(index).fadeOut(1000);
        $obj2.eq(index).removeClass('activate');
        index = num;
        $obj1.eq(index).fadeIn(1000);
        $obj2.eq(index).addClass('activate');
    };
    //小圆点点击事件
    $select.click(function () {
        var num = $(this).index();
        if (num != index) {
            change($img, $select, num);
        }
        ;
    });
    //左右箭头点击事件
    $btn.click(function () {
        var num = index;
        if ($(this).index()) {
            num++
        }
        else {
            num--
        }
        ;
        num = num % len;
        change($img, $select, num);
    });

    //定时轮播图片
    function f() {
        var num = index;
        num++;
        num = num % len;
        change($img, $select, num);
    }

    var SI = setInterval(f, 3000);
    $banner.hover(function () {
        clearInterval(SI)
    }, function () {
        SI = setInterval(f, 3000)
    });
});
$(function () {
    //菜单栏
    function change($obj1, $obj2, num) {
        $obj1.eq(index).fadeOut(1000);
        $obj1.eq(index).removeClass('activate');
        $obj2.eq(index).removeClass('activate');
        index = num;
        $obj1.eq(index).fadeIn(1000);
        $obj1.eq(index).addClass('activate');
        $obj2.eq(index).addClass('activate');
    }

    var $title = $('.menus .title li');
    var $content = $('.menus .menus-con li');
    var index = 0;
    // 初始化给第一个标签添加蓝色粗线index=0
    change($content, $title, index);
    $title.click(function () {
        var number = $(this).index();
        change($content, $title, number);
    })


});

// 加载更多
$(function () {
    // ========== 获取元素 ========
    // content 盒子
    let $content = $(".menus");
    // newsContain 盒子
    let $newsContain = $(".news-contain");
    // 加载更多的按钮
    let $moreBtn = $(".load_multi");
    // 获取所有的新闻分类
    let $li = $('.title li');

    // 将jq 对象转为 js 对象 使用原生 JS 是 addEventListener 注册点击事件
    $moreBtn[0].addEventListener('click', function () {
        // 添加一个 loading
        $newsContain.append(`<div class="loading-img"></div>`);
        // 获取loading
        let $loadImg = $(".loading-img");
        // 找到已经被激活的新闻分类下面的 a 标签
        let tagId = $('.title li.activate').data("id");
        // 获取绑定在按钮上的页码
        let page = $(this).data("page");
        // 打印值
        console.log(`
      当前所处在分类id  ${tagId}
      当前第几页  ${page}    
    `);
        // 发起 get 的请求 也可以写成 $.get(`/news/list/?page=${page}&tag_id=${tagId}`, res=>{}) 方式
        $.get({
            // 请求的 url
            url: "/news/list/",
            // 发送的数据
            data: {
                "page": page,
                "tag_id": tagId,
            },
            // 成功之后的回调函数
            success: res => {
                if (res["code"] === 1) {
                    // 获取数据
                    let data = res["data"];
                    // 获取新闻列表
                    let newses = data["newses"];
                    console.log(newses);
                    if (newses.length > 0) {
                        // 遍历
                        newses.forEach((news) => {
                            console.log(news);
                            // 获取新闻发布时间
                            let pub_time = news["add_time"];
                            // 格式化新闻发布时间
                            let result = dateFormat(pub_time);
                            let newsStr = `
                                    <div class="info">
                                        <div class="pic">
                                            <img src=${news.photo_url}>
                                        </div>
                                        <div class="text">
                                            <h4><a href="/news/news_detail/${news.id}" target="_blank" style="color: #000000;">${news.title}</a></h4>
                                            <p>${news.desc}</p>
                                            <div class="other">
                                                <span class="hot">${news.tag.tag_name}</span>
                                                <span class="time">${result}</span>
                                                <span class="author">${news.author.username}</span>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            // 获取新闻列表
                            let $newsList = $(".menus-con .activate");
                            $newsList.append(newsStr);
                        })
                    } else {
                        // 如果点击加载更多 已无新闻 则移除自己
                        $(this).remove();
                    }
                    // 移除 loading
                    $loadImg.remove();
                }
                // 点一次 page +1 并绑定到data-page 上
                page++; // page
                $(this).data("page", page);
            },
            error: err => {
                logError(err);
            }
        })
    });


    // 点击切换分类执行的时间
    $li.click(function () {
        // 点击那个 则为点击的加上一个class名字 active 并移除其它兄弟元素的上的 class名字是active的
        $(this).addClass('active').siblings('li').removeClass('active');
        // 获取绑定在当前选中分类上的 id字段
        let tagId = $(this).data('id');
        // 设置点击加载更多的默认值为2
        $moreBtn.data("page", 2);
        // 发起 get 请求
        $.get({
            url: "/news/list/",
            data: {
                "tag_id": tagId,
            },
            success: res => {
                if (res["code"] === 1) {
                    let data = res["data"];
                    let newses = data["newses"];
                    // 每次加载前提前清空当前分类下的所有新闻
                    // 获取新闻列表
                    let $newsList = $(".menus-con .activate");
                    $newsList.children().remove();
                    if (newses.length > 0) {
                        newses.forEach(news => {
                            let pub_time = news["add_time"];
                            let result = dateFormat(pub_time);
                            // `` 模板字符串 ${news.title}
                            let newsStr = `
                                <div class="info">
                                    <div class="pic">
                                    <img src=${news.photo_url}>
                                    </div>
                                    <div class="text">
                                        <h4><a href="/news/news_detail/${news.id}" target="_blank" style="color: #000000;">${news.title}</a></h4>
                                        <p>${news.desc}</p>
                                        <div class="other">
                                            <span class="hot">${news.tag.tag_name}</span>
                                            <span class="time">${result}</span>
                                            <span class="author">${news.author.username}</span>
                                        </div>
                                    </div>
                                </div>
                                `;
                            $newsList.append(newsStr);
                            $content.append($moreBtn);
                        })
                    } else {
                        $moreBtn.remove();
                    }
                }
            }
        })
    });
});
/*======= 日期格式化 =======*/
function dateFormat(time) {
    // 获取当前的时间戳
    let timeNow = Date.now();
    // 获取发表文章的时间戳
    let TimeStamp = new Date(time).getTime();
    // 转为秒
    let second = (timeNow - TimeStamp) / 1000;
    if (second < 60) {
        return '刚刚'
    } else if (second >= 60 && second < 60 * 60) {
        let minute = Math.floor(second / 60);
        return `${minute}分钟前`;
    } else if (second >= 60 * 60 && second < 60 * 60 * 24) {
        let hour = Math.floor(second / 60 / 60);
        return `${hour}小时前`;
    } else if (second >= 60 * 60 * 24 && second < 60 * 60 * 24 * 30) {
        let day = Math.floor(second / 60 / 60 / 24);
        return `${day}天前`;
    } else {
        let date = new Date(TimeStamp);
        let Y = date.getFullYear() + '/';
        let M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '/';
        let D = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate()) + ' ';
        let h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':';
        let m = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes());
        return Y + M + D + h + m;
    }
}