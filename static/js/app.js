$(document).ready(function () {
	const example = flatpickr('#flatpickr', {
		inline: true,
		enableTime: false,
		dateFormat: "d-m-Y",
		monthSelectorType: 'static',
		yearSelectorType: 'static',
		onChange: function (date) {
			const selected_date = moment(date[0]).format('DD-MM-YYYY')
			setSelectedDate(selected_date);
			const doctor_id = getDoctorId();
			location.href = `/calendar/${doctor_id}/${selected_date}`;

		},
		onClose: function () {
			$('#flatpickr').blur() // Necessary to fix flatpickr bug that causes picker to open automatically
		}
	});

	$('.sidebarCollapse, .overlay').on('click', function () {
		$('#sidebar').toggleClass('active');
		$('.overlay').toggleClass('active');
	});

	// Close the sidebar on page load if screenwidth is <= 798.
	if ($(window).width() <= 798) {
		$('#sidebar').toggleClass('active')
	}


	// Open or close the sidebar when screen is resized around the specified breakpoint
	window.matchMedia('(max-width: 798px)').addListener(function (e) {
		if (e.matches) {
			$('#sidebar').toggleClass('active')
		} else {
			$('#sidebar').removeClass('active')
			$('.overlay').removeClass('active');
		}
	})

    // New appointment modal
	$('#newAppointmentModal').on('show.bs.modal', function (event) {
		const slot = $(event.relatedTarget); // Slot that triggered the modal
		const startTime = slot.data('time');
		const modal = $(this);
        const endTimeElement = $("#newApptEndTime");
        setAvailableSlotTimes(startTime,endTimeElement);

        modal.find('#startTime').val(startTime); // Add the selected slot time to the modal input
	})

    // Edit appointment setAvailableSlotTimes(startTime,endTimeElement);modal
	$('#editAppointmentModal').on('show.bs.modal', function (event) {
		const slot = $(event.relatedTarget); // Slot that triggered the modal
		//console.startlog($(slot).children('.patient-name').innerText())
        const modal = $(this);
		const startTime = slot.data('start');
		const endTimeElement = $("#editApptEndTime");
		const currentAppointmentId = slot.data('id')
		setAvailableSlotTimes(startTime,endTimeElement, currentAppointmentId);
		const endTime = moment.utc(slot.data('end'), 'HH:mm').add(15, 'minutes').format('HH:mm')


		const dayId = $(".calendar-container").data('dayid')

		modal.find('#day_id').val(dayId)
		modal.find('#appointment_id').val(currentAppointmentId)
		modal.find('#startTime').val(startTime); // Add the selected slot time to the modal input
	})


	/*$('#add-appointment').on('click', function () {
		console.log("Test")
	})*/


	// Event handler for selecting a doctor via dropdown list
	$("#select-doc").on("click", function () {
		const selectDoctorElement = $(".js-example-basic-single")
		const doctorId = selectDoctorElement.val();
		changeDoctor(doctorId)
	})

	// Event handler for selecting a doctor via entry page divs
	$(".doc-container").on("click", function () {
		const doctorId = $(this).data("docid")
		changeDoctor(doctorId)
	})


	function changeDoctor(doctorId) {
		setDoctorId(doctorId); // add doctor id to local storage
		const selected_date = getSelectedDate()
		console.log("selected date:" + selected_date)
		if (selected_date) {
			location.href = `/calendar/${doctorId}/${selected_date}`;
		} else {
			location.href = `/calendar/${doctorId}`
		}
	}

	function setAvailableSlotTimes(startTime, endTimeElement, currentAppointmentId = ""){
	    console.log("Inside set slots")
	    const allSubsequentSlots = $(".slot").map(function () {
			const slotTime = $(this).data("time")
			const startSlotTime = new Date("1980-01-01 " + startTime);
			const otherSlotTime = new Date("1980-01-01 " + slotTime);
			if ((otherSlotTime >= startSlotTime)) {
				return this
			}
		})
        console.log(allSubsequentSlots)
        endTimeElement.empty()
		for (i = 0; i < allSubsequentSlots.length; i++) {
			const slotTime = $(allSubsequentSlots[i]).data("time")
			const appointmentId = $(allSubsequentSlots[i]).data("id")
			if (!appointmentId || (appointmentId == currentAppointmentId)) {
				console.log("inside if")
				const displayTime = moment.utc(slotTime, 'HH:mm').add(15, 'minutes').format('HH:mm')
				endTimeElement.append(`<option value=${slotTime}>${displayTime}</option>`)

			} else {
				break;
			}
		}
    }

	function setDoctorId(doctorId) {
		localStorage.setItem("selected_doctor_id", doctorId);
	}

	function getDoctorId() {
		return localStorage.getItem("selected_doctor_id")
	}

	function setSelectedDate(selectedDate) {
		localStorage.setItem("selected_date", selectedDate);
	}

	function getSelectedDate() {
		return localStorage.getItem("selected_date")
	}

});