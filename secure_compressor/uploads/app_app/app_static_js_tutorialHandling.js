let previousPopup = null;

const handleShowContent = (disable, enable) => {
    document.getElementById(disable).classList.toggle("disabledSlide");
    for (let i = 0; i < enable.length; i++){
        document.getElementById(enable[i]).classList.toggle("disabledSlide");
    }
}

function showStep () {
    let step = parseInt(sessionStorage.getItem("tutorialStep")) || 0;
    let popup = document.createElement("p");
    let parentElement;
    if (previousPopup) {
        previousPopup.remove();
    }
    switch(step) {
        case 0:
            sessionStorage.setItem("tutorialStep", 0);
            parentElement = document.getElementById("sidebar");
            popup.classList = "step top left";
            popup.innerText = "This is the sidebar. Here, you can see the different phases. From here, you can also have access to the tips page if you want to look up how a specific phase works.";
            alignRightTopToParent(popup, parentElement);
            break;
        case 1:
            parentElement = document.getElementById("planning");
            popup.classList = "step middle left";
            popup.style.marginTop = "-10px";
            popup.innerText = "This is the planning section. In this phase, I'll guide you with questions to help you create a clear plan. I won't give you answers but will help you outline your goals and tasks.";
            alignRightMiddleToParent(popup, parentElement);
            break;
        case 2: 
            parentElement = document.getElementById("monitoring");
            popup.classList = "step top left";
            popup.innerText = "This is the monitoring section. Once your plan is set, you'll update me on your progress. If you fall off track, I'll provide tips and help you adjust your schedule to stay on course. The phase is currently disabled. You have to finish the planning section first to gain access to the monitoring section.";
            alignRightMiddleToParent(popup, parentElement);
            break;
        case 3: 
            parentElement = document.getElementById("reflecting");
            popup.classList = "step top left";
            popup.innerText = "This is the reflecting section. After completing your tasks, we'll reflect on your work. I'll ask questions to help you identify what went well, what didn't, and what you can learn for next time. You have to finish the monitoring section first to gain access to the reflecting section.";
            alignRightMiddleToParent(popup, parentElement);
            break;
        case 4: 
            parentElement = document.getElementById("tips");
            popup.classList = "step bottom left";
            popup.style.marginBottom = "-10px";
            popup.innerText = "This is the tips section. If you want to look up how the phases work, this is your place to go.";
            alignRightBottomToParent(popup, parentElement);
            break;
        case 5:
            parentElement = document.getElementById("help");
            popup.classList = "step topTop leftTop";
            popup.style.marginBottom = "15px";
            popup.innerText = "This is the help section. If you want to know more about the AI Tutor you'll get the information here";
            alignTopLeftToParent(popup, parentElement);
            break;
        case 6:
            parentElement = document.getElementById("promptInput");
            popup.classList = "step topTop middleTop";
            popup.style.marginBottom = "5px";
            popup.innerText = "This is the inputfield. Here you can enter a prompt and I'll answer you.";
            alignTopMiddleToParent(popup, parentElement);
            break;
        case 7:
            parentElement = document.getElementById("menu");
            popup.classList = "step top leftLeft";
            popup.style.marginBottom = "5px";
            popup.innerText = "This is the menu. Here you can go to the help page, log out and switch between dark and light mode.";
            alignLeftTopToParent(popup, parentElement);
            break;
        case 8:
            parentElement = document.getElementById("tutorial2prompt");
            popup.classList = "step top leftLeft";
            popup.innerText = "This is our chat. Here you can see your prompts and my answers.";
            alignTopToParent(popup, parentElement)
            break;
        case 9:
            const parent = document.getElementById("messages1");
            console.log(parent)
            popup = addAnswer("We are now finished with the tutorial. Click on next to start planning!")
            parent.appendChild(popup);
            break;
        case 9:
            //TODO: redirect to main page
            //window.location.href = "../../templates/main.html"
        default:
            console.warn("Step not recognized:", step);
            return;
    }
    previousPopup = popup;
}

function addAnswer(message) {
    const answerContainer = document.createElement("div");
    answerContainer.className = "answer_container";
    answerContainer.innerHTML = `
        <div class="icon logo">
            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000">
                <path d="M280-280h160v-160H280v160Zm240 0h160v-160H520v160ZM280-520h160v-160H280v160Zm240 0h160v-160H520v160ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"/>
            </svg>
        </div>
    `;
    const text = document.createElement("DIV");
    text.className = "answer";
    text.innerHTML = message
    answerContainer.appendChild(text);
    return answerContainer;

}

function alignRightTopToParent(popup, parentElement) {
    if (parentElement) {
        const rect = parentElement.getBoundingClientRect();
        popup.style.position = "absolute";
        popup.style.top = `${rect.top + window.scrollY}px`;
        popup.style.left = `${rect.right + window.scrollX}px`;
        popup.style.display = "block"; 
        document.body.appendChild(popup);
    } else {
        console.error("Parent element not found");
    }
}

function alignRightMiddleToParent(popup, parentElement) {
    if (parentElement) {
        const rect = parentElement.getBoundingClientRect();
        popup.style.position = "absolute";
        popup.style.top = `${rect.top + window.scrollY - rect.height / 2}px`;
        popup.style.left = `${rect.right + window.scrollX}px`;
        popup.style.display = "block"; 
        document.body.appendChild(popup);
    } else {
        console.error("Parent element not found");
    }
}

function alignRightBottomToParent(popup, parentElement) {
    if (parentElement) {
        const rect = parentElement.getBoundingClientRect();
        let parentBottom = window.innerHeight - rect.bottom;
        popup.style.position = "absolute";
        popup.style.bottom = `${parentBottom}px`;
        popup.style.left = `${rect.right + window.scrollX}px`;
        popup.style.display = "block"; 
        document.body.appendChild(popup);
    } else {
        console.error("Parent element not found");
    }
}

function alignTopLeftToParent(popup, parentElement){
    if (parentElement) {
        const rect = parentElement.getBoundingClientRect();
        popup.style.position = "absolute";
        popup.style.bottom = `${window.innerHeight - rect.top + 10}px`;
        popup.style.left = `${parseInt(rect.left/4)}px`;
        popup.style.display = "block";
        document.body.appendChild(popup);
    } else {
        console.error("Parent element not found");
    }
}

function alignTopToParent(popup, parentElement){
    if (parentElement) {
        const rect = parentElement.getBoundingClientRect();
        popup.style.position = "absolute";
        popup.style.top = `${rect.top}px`;
        popup.style.left = `${parseInt(rect.left/5)}px`;
        popup.style.display = "block";
        document.body.appendChild(popup);
    } else {
        console.error("Parent element not found");
    }
}

function alignTopMiddleToParent(popup, parentElement){
    if (parentElement) {
        const rect = parentElement.getBoundingClientRect();
        popup.style.position = "absolute";
        popup.style.bottom = `${window.innerHeight - rect.top}px`;
        popup.style.left = `${parseInt(rect.left)}px`;
        popup.style.display = "block";
        document.body.appendChild(popup);
    } else {
        console.error("Parent element not found");
    }
}
function alignLeftTopToParent(popup, parentElement) {
    if (parentElement) {
        const rect = parentElement.getBoundingClientRect();
        console.log(parentElement.lastElementChild.width)
        popup.style.position = "absolute";
        popup.style.top = `${rect.top + window.scrollY}px`;
        popup.style.display = "block"; 
        document.body.appendChild(popup);
    } else {
        console.error("Parent element not found");
    }
}
function increaseStep () {
    console.log("Next")
    let step = parseInt(sessionStorage.getItem("tutorialStep"));
    if (step < 9){
        step +=1;
    }
    sessionStorage.setItem("tutorialStep", step);
    showStep()
}

function decreaseStep () {
    let step = parseInt(sessionStorage.getItem("tutorialStep"));
    if (step > 0){
        step -= 1;
        sessionStorage.setItem("tutorialStep", step);
    }
    showStep()
}
document.getElementById("tutorial1Next").addEventListener("click", () => handleShowContent("tutorial1", ["tutorial2", "stepButtons"]));
document.getElementById("tutorial1Next").addEventListener("click", () => showStep());
document.getElementById("nextStep")?.addEventListener("click", () => increaseStep());
document.getElementById("backStep")?.addEventListener("click", () => decreaseStep());
document.getElementById("submit")?.addEventListener("click", function(event){
    event.preventDefault()
  });

