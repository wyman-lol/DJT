$(function(){
    //菜单栏
    function change($obj1,$obj2,num){
        $obj1.eq(index).fadeOut(1000);
        console.log($obj1.eq(index))
        $obj2.eq(index).removeClass('activate');
        index = num;
        $obj1.eq(index).fadeIn(1000);
        $obj2.eq(index).addClass('activate');
    };
    var $title=$('.menu .title li');
    var $content=$('.mid-con .con-list .con');
    var index=0;
    $title.click(function(){
        var number = $(this).index();
        change($content,$title,number);
    })
})