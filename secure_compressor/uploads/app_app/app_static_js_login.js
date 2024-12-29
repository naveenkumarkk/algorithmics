import GeneralFunctions from "./GeneralFunctions.js";

const generalFunctions = new GeneralFunctions();

function handleLogin (event) {
    event.preventDefault();

    const form = document.getElementById("login");

    const formData = new FormData(form);
    const username = formData.get("username");
    const password = formData.get("password");

    localStorage.setItem("activeElement", "planning");

    //TODO validating
    window.location.href = "/chatgpt/chatscreen";
}

window.onload = async function () {
    generalFunctions.toggleDarkmode();
    generalFunctions.googleAuthentication();
}

// document.getElementById("login").addEventListener("submit", handleLogin);
