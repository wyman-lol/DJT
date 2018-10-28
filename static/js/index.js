$(function(){
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
    function change($obj1,$obj2,num){
        $obj1.eq(index).fadeOut(1000);
        $obj2.eq(index).removeClass('activate');
        index = num;
        $obj1.eq(index).fadeIn(1000);
        $obj2.eq(index).addClass('activate');
    };
    //小圆点点击事件
    $select.click(function(){
        var num = $(this).index();
        if(num != index){
            change($img,$select,num);
        };
    });
    //左右箭头点击事件
    $btn.click(function(){
        var num = index;
        if($(this).index()){
            num++
        }
        else{
            num--
        };
        num = num%len;
        change($img,$select,num);
    });
    //定时轮播图片
    function f(){
        var num = index;
        num++;
        num = num%len;
        change($img,$select,num);
    }
    var SI=setInterval(f,3000);
    $banner.hover(function(){clearInterval(SI)},function(){SI=setInterval(f,3000)});
});
$(function(){
    //菜单栏
    function change($obj1,$obj2,num){
        $obj1.eq(index).fadeOut(1000);
        $obj2.eq(index).removeClass('activate');
        index = num;
        $obj1.eq(index).fadeIn(1000);
        $obj2.eq(index).addClass('activate');
    }
    var $title=$('.menus .title li');
    var $content=$('.menus .menus-con li');
    var index=0;
    // 初始化给第一个标签添加蓝色粗线index=0
    change($content,$title,index);
    $title.click(function(){
        var number = $(this).index();
        change($content,$title,number);
    })
});