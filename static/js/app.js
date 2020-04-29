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
       modal.find('.modal-body input').val(time)
    })
});
