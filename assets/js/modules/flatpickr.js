import flatpickr from "flatpickr";
import rangePlugin from "../plugins/flatpickr/plugins/rangePlugin.ts";

document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll(".datepicker").forEach(element => {
		let args = JSON.parse(element.dataset.flatpickr_args);

		if(element.hasAttribute('data-range_second_input')){
			let secondInput = document.querySelector(element.dataset.range_second_input);
			secondInput.removeAttribute('name');
			args["plugins"] = [new rangePlugin({ input: element.dataset.range_second_input})]
		}
		let fp = flatpickr(element, args);
	});
});