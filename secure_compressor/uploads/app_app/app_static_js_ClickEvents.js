import LoadData from "./LoadData.js";
const loadDataFromBackend = new LoadData();
class ClickEvents {

    clickPlanning() {
        if (localStorage.getItem('allowPlanningPhase') == 'true') {
            if (localStorage.getItem('activeElement') !== 'planning' && localStorage.getItem('activeElement') !== '' && localStorage.getItem('activeElement') !== 'tips') {
                document.getElementById("promptInput").classList.remove("hidden");
            }
            
            let currentElement = document.getElementsByClassName("on");
            if (currentElement.length == 1 && currentElement[0].id != "planning") {
                currentElement[0].classList.toggle("on");
            }
            document.getElementById("planning").classList.toggle("on");
            localStorage.setItem("activeElement", "planning");
            // loadDataFromBackend.updateNextPhaseStatus()
        } else {
            alert("You have an ongoing conversation! Complete that and comeback to planning phase for new conversation")
        }

    }

    clickMonitoring() {
        if (localStorage.getItem('allowMonitoringPhase') == 'true') {
            if (localStorage.getItem('activeElement') !== 'monitoring'  && localStorage.getItem('activeElement') !== '' && localStorage.getItem('activeElement') !== 'tips') {
                document.getElementById("promptInput").classList.remove("hidden");
            }
            let currentElement = document.getElementsByClassName("on");
            if (currentElement.length == 1 && currentElement[0].id != "monitoring") {
                currentElement[0].classList.toggle("on");
            }
            document.getElementById("monitoring").classList.toggle("on");
            localStorage.setItem("activeElement", "monitoring");
            // loadDataFromBackend.updateNextPhaseStatus()
        } else {
            alert("Complete the planning phase!")
        }
    }

    clickReflecting() {
        if (localStorage.getItem('allowReflectionPhase') == 'true') {
            if (localStorage.getItem('activeElement') !== 'reflecting'  && localStorage.getItem('activeElement') !== '' && localStorage.getItem('activeElement') !== 'tips') {
                document.getElementById("promptInput").classList.remove("hidden");
            }
            let currentElement = document.getElementsByClassName("on");
            if (currentElement.length == 1 && currentElement[0].id != "reflecting") {
                currentElement[0].classList.toggle("on");
            }
            document.getElementById("reflecting").classList.toggle("on");
            localStorage.setItem("activeElement", "reflecting");
            // loadDataFromBackend.updateNextPhaseStatus()
        } else {
            alert("Complete the Monitoring phase!")
        }
    }

    clickTips(event) {
        localStorage.setItem("activeElement", "tips");
        window.location.href = "/chatgpt/tips";
    }
}

export default ClickEvents;