$(document).ready(function() {
   /** $(".remove").click(function(){
        const id = $(this).attr("data-id");
        const url = "/remove_appointment/".concat(id);
        location.href=url;
        })

    $('#myTabs a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')**/


$('#newAppointmentModal').on('show.bs.modal', function (event) {
    const slot = $(event.relatedTarget); // Slot that triggered the modal
    const time = slot.data('time');
    const modal = $(this);
    modal.find('.modal-body input').val(time); // Add the selected slot time to the modal input

    const otherSlots = $(".slot").map(function (){
        const slotTime = $(this).data("time")
        console.log("other slot time:" + slotTime)
            const base = new Date("1980-01-01 " + time);
            const test = new Date("1980-01-01 " + slotTime);
            if ((test > base)) {
                return this }
    })

    const availableTimes = [];
    const endTimeList = $("#endTime");
    endTimeList.empty()
    for(i=0; i < otherSlots.length; i++){
        const slotTime = $(otherSlots[i]).data("time")
        const appointmentId = $(otherSlots[i]).data("id")
        if(!appointmentId){
            $("#endTime").append(`<option value=${slotTime}>${slotTime}</option>`)
            availableTimes.push(slotTime)}
        else { break;}
          }



})
});
     /****test***
    var base = new Date("1980-01-01 09:30");
    var test = new Date("1980-01-01 08:30:01");

    if (test >= base){
    console.log("test time is newer or equal to base time");

}   else {
    console.log ("test time is older than 9.30");

}*/


