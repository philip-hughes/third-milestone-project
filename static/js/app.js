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
            if ((test >= base)) {
                return this }
    })


    const endTimeList = $("#endTime");
    endTimeList.empty()
    for(i=0; i < otherSlots.length; i++){
        const slotTime = $(otherSlots[i]).data("time")
        const appointmentId = $(otherSlots[i]).data("id")
        if(!appointmentId){
            const displayTime = moment.utc(slotTime,'HH:mm').add(15,'minutes').format('HH:mm')
            endTimeList.append(`<option value=${slotTime}>${displayTime}</option>`)}
        else { break;}
          }

})

$('#editAppointmentModal').on('show.bs.modal', function (event) {
    const slot = $(event.relatedTarget); // Slot that triggered the modal
    const time = slot.data('time');
    const modal = $(this);
    const id = slot.data('id')
    modal.find('.modal-body input').val(time); // Add the selected slot time to the modal input
    modal.find(".modal-body a").attr("href", `/remove_appointment/${id}`)

    const otherSlots = $(".slot").map(function (){
        const slotTime = $(this).data("time")
        console.log("other slot time:" + slotTime)
            const base = new Date("1980-01-01 " + time);
            const test = new Date("1980-01-01 " + slotTime);
            if ((test >= base)) {
                return this }
    })


    const endTimeList = $("#endTime");
    endTimeList.empty()
    for(i=0; i < otherSlots.length; i++){
        const slotTime = $(otherSlots[i]).data("time")
        const appointmentId = $(otherSlots[i]).data("id")
        if(!appointmentId){
            const displayTime = moment.utc(slotTime,'HH:mm').add(15,'minutes').format('HH:mm')
            endTimeList.append(`<option value=${slotTime}>${displayTime}</option>`)}
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


