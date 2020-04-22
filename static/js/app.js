$(document).ready(function() {
    $(".remove").click(function(){
        const id = $(this).attr("data-id");
        const url = "/remove_appointment/".concat(id);
        location.href=url;
        })
});