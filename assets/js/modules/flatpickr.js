import flatpickr from "flatpickr";

document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll(".datepicker").forEach(element => {
		let args = JSON.parse(element.dataset.flatpickr_args);
		flatpickr(element, args);
	});
});