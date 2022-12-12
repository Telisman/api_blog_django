var sighnUpButton = document.querySelector('#signUp');
var sighnInButton = document.querySelector('#signIn');
var container = document.querySelector('#container');


sighnUpButton.addEventListener('click', () => {
 container.classList.add('right-panel-active');
});
sighnInButton.addEventListener('click', () => {
 container.classList.remove('right-panel-active');
});