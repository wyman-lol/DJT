/*===  navMenuStart ===*/
$(() => {
    let $navLi = $('#header .nav .menu li')
    $navLi.click(function () {
        $(this).addClass('active').siblings('li').removeClass('active')
    });
});

/*===  navMenuEnd ===*/

/*== logErrorStart ==*/
function logError(err) {
    console.log(err);
    console.log(err.status + "===" + err.statusText);
}
/*== logErrorEnd ==*/
