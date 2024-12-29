import ClickEvents from "./ClickEvents.js";
import GeneralFunctions from "./GeneralFunctions.js";
import LoadData from "./LoadData.js";

const click = new ClickEvents();
const loadData = new LoadData();
const generalFunctions = new GeneralFunctions();

function clickPlanning (event) {
    click.clickPlanning();
    window.location.href = "/chatgpt/chatscreen";
}

function clickMonitoring (event) {
    click.clickMonitoring();
    window.location.href = "/chatgpt/chatscreen";
}

function clickReflecting (event) {
    click.clickReflecting();
    window.location.href = "/chatgpt/chatscreen";
}

window.onload = async function () {
    localStorage.setItem("activeElement", "tips");
    loadData.updateNextPhaseStatus();
    generalFunctions.toggleDarkmode();
}

document.getElementById("planning").addEventListener("click", clickPlanning);
document.getElementById("monitoring").addEventListener("click", clickMonitoring);
document.getElementById("reflecting").addEventListener("click", clickReflecting);