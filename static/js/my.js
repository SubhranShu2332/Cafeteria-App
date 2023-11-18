const resizer = document.getElementById('resizer');
const sidebar = document.getElementById('sidebar');
const userDetails = document.getElementById('userDetails');
const company_name = document.getElementById('company_name');
const menu_name = document.querySelectorAll('.menu_name');
const darkLight = document.getElementById('dark-light');
const resizeHandler = (e) => {
    const size = `${e.x}px`;
    for (let i = 0; i < menu_name.length; ++i) {
        if (e.x < 100) {
            menu_name[i].classList.add('deactive')
        } else {
            menu_name[i].classList.remove('deactive')
        }
    }
    if (e.x < 100) {
        company_name.classList.add('deactive')
    } else {
        company_name.classList.remove('deactive')
    }
    if (e.x > 250) {
        userDetails.classList.add('active')
    } else {
        userDetails.classList.remove('active')
    }
    sidebar.style.flexBasis = size;
}
resizer.addEventListener('mousedown', () => {
    document.addEventListener('mousemove', resizeHandler, false);
    document, addEventListener('mouseup', () => {
        document.removeEventListener('mousemove', resizeHandler, false)
    }, false)
});
darkLight.addEventListener('click', () => {
    darkLight.classList.toggle('fa-sun');
    document.body.classList.toggle('dark_colors')
})