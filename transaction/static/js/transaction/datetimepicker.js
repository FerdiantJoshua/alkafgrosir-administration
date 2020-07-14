$(document).ready(function() {
    const useTimePicker = false
    const dateFormat = 'd-m-Y'

    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = dd + '/' + mm + '/' + yyyy

    $('#id_date').datetimepicker({
        timepicker: useTimePicker,
        format: dateFormat,
    });

    $('#id_date_start').datetimepicker({
        timepicker: useTimePicker,
        format: dateFormat,
        onShow:function( ct ){
         this.setOptions({
          maxDate:$('#id_date_end').val()?$('#id_date_end').val():false,
//          value:$('#id_date_end').val()?$('#id_date_end').val():self.val()
         })
        },
    });
    $('#id_date_end').datetimepicker({
        timepicker: useTimePicker,
        format: dateFormat,
        onShow:function( ct ){
         this.setOptions({
          minDate:$('#id_date_start').val()?$('#id_date_start').val():false
         })
        },
    });
})