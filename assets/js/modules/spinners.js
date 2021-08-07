
document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll(".spinner-btn").forEach(element => {
		let spinner = document.createElement('div');
		spinner.classList.add('spinner', 'spinner-hidden');
		
		element.addEventListener('click', function(e){
			//if contained in form. Make sure form is valid before spinning
			let form = e.currentTarget.closest('form');
			if(form && form.checkValidity()){
				element.querySelector('.spinner').classList.toggle('spinner-hidden');
			}else if(!form){
				element.querySelector('.spinner').classList.toggle('spinner-hidden');
			}
		});
		element.prepend(spinner);
	});
});