$(document).ready(function() {
  $('#id_date, #id_date_start, #id_date_end').datepicker({
    format: "dd-mm-yyyy",
    maxViewMode: 2,
    todayBtn: "linked",
    clearBtn: true,
    daysOfWeekHighlighted: "0",
    autoclose: true,
    todayHighlight: true,
    toggleActive: true
  })
})