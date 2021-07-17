
document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll(".spinner-btn").forEach(element => {
		let spinner = document.createElement('div');
		spinner.classList.add('spinner', 'spinner-hidden');
		
		element.addEventListener('click', function(e){
			element.querySelector('.spinner').classList.toggle('spinner-hidden');
		});
		element.prepend(spinner);
	});
});