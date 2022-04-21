document.addEventListener("DOMContentLoaded", () => {
	let dateElem = document.querySelector('#year-date')
	if (dateElem !== null){
		dateElem.innerHTML = new Date().getFullYear();
	};
});