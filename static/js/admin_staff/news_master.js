$(function () {
  let startTime = $("input[name=start_time]");
  let endTime = $("input[name=end_time]");
  const config = {
    // 自动关闭
    autoclose: true,
    // 日期格式
    format: 'yyyy/mm/dd',
    // 选择语言为中文
    language: 'zh-CN',
    // 优化样式
    showButtonPanel: true,
    // 高亮今天
    todayHighlight: true,
    // 是否在周行的左侧显示周数
    calendarWeeks: true,
    // 清除
    clearBtn: true,
    // 0 ~11  网站上线的时候
    startDate: new Date(2018, 7, 20),
    // 今天
    endDate: new Date(),
  };
  startTime.datepicker(config);
  endTime.datepicker(config);
});