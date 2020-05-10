$(document).ready(function() {

const selectDoctorElement = $(".js-example-basic-single")
$("#select-doc").on("click",function(){
    const doctorId = selectDoctorElement.val();
    location.href = `/set_doctor/${doctorId}`
})

const example = flatpickr('#flatpickr', {
    inline: true,
    enableTime: false,
    dateFormat: "d-m-Y",
    monthSelectorType: 'static',
    yearSelectorType: 'static',
    onChange: function(date){
        const selected_date = moment(date[0]).unix()
        location.href = `/set_date/${selected_date}`;
    },
    onClose: function(){
        $('#flatpickr').blur()
    }
   });


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
    const startTime = slot.data('start');
    const endTime = moment.utc(slot.data('end'),'HH:mm').add(15,'minutes').format('HH:mm')
    const modal = $(this);
    const id = slot.data('id')
    const dayId = $(".calendar-container").data("dayid")
    modal.find('.modal-body #startTime').text(startTime);
    modal.find('.modal-body #endTime').text(endTime); // Add the selected slot time to the modal input
    modal.find(".modal-body a").attr("href", `/remove_appointment/${id}/${dayId}`)
})

function setDoctorId(doctorId){
    localStorage.setItem("selected_doctor_id", doctorId);
}

});



