
document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll(".sticky-sidebar.translate-middle-y").forEach(element => {
		let top = (element.offsetHeight /2);
		element.style.top = top + "px";
	});
});