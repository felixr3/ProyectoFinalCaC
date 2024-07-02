const header = document.querySelector('header')

window.addEventListener('scroll', () => {
  header.classList.toggle('sticky', this.window.scrollY > 80)
})

// Desplazamiento suave hacia arriba
function scrollToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

//Menu
let menu = document.querySelector('#menu-icono');
let navegacion = document.querySelector('.navegacion');

menu.onclick = () => {
  menu.classList.toggle('bx-x');
  navegacion.classList.toggle('open');
}

window.onscroll = () => {
  menu.classList.remove('bx-x');
  navegacion.classList.remove('open')
}
