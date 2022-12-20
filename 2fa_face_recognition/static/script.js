const wrapper = document.querySelector('.wrapper');
const signUpLink = document.querySelector('.SignUp-link');
const signInLink = document.querySelector('.SignIn-link');
const toggleLogin = document.querySelector('.toggle-login');
const title_first = document.querySelector('.first-part');
const title_second = document.querySelector('.second-part');
const close = document.querySelector('.close');

signUpLink.addEventListener('click', function()
{
    if(wrapper.classList.contains('dsp-sign'))
        wrapper.classList.remove('dsp-sign');
    wrapper.classList.add('show-sign');
    wrapper.classList.add('show-bg');
});

signInLink.addEventListener('click', function()
{
    if(wrapper.classList.contains('show-sign'))
        wrapper.classList.remove('show-sign');
    wrapper.classList.add('dsp-sign');
    wrapper.classList.add('show-bg');
});

toggleLogin.addEventListener('click', function()
{
    title_first.classList.toggle('active');
    title_second.classList.toggle('active');
    toggleLogin.classList.toggle('active');
    wrapper.classList.toggle('active');
});

close.addEventListener('click', function()
{
    title_first.classList.remove('active');
    title_second.classList.remove('active');
    toggleLogin.classList.toggle('active');
    wrapper.classList.toggle('active');
    wrapper.classList.remove('dsp-sign');
    wrapper.classList.remove('show-sign');
    wrapper.classList.remove('show-bg');
});