function buttonMenu(obj) {
	obj1 = obj.nextElementSibling;
	if(obj.nextElementSibling.style.display === 'block'){
		obj.querySelector('#arrow').style.transform = 'rotate(0deg)';
		obj1.style.display = 'none'
		obj.style.background = '#263959';
		obj.style.color = 'white';
	}else {
		obj.querySelector('#arrow').style.transform = 'rotate(-90deg)';
		obj1.style.display = 'block';
		obj.style.background = '#f2efe6';
		obj.style.color = '#263959';
	}
}
