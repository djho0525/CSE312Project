function showLogin(){
    elem=document.getElementById("loginForm")
    elem.style.display = "block"
    hideElem=document.getElementById("signUpForm")
    hideElem.style.display = "none"
}

function showSignup(){
    elem=document.getElementById("signUpForm")
    elem.style.display = "block"
    hideElem=document.getElementById("loginForm")
    hideElem.style.display = "none"
}