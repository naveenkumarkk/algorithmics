class LoadData {

    clear() {
        const parent = document.getElementsByClassName("messages")[0];
        parent.innerHTML = '';
    }

    loadData() {
        const activeElement = localStorage.getItem("activeElement");

        if (activeElement === "monitoring") {
            document.title = "AI Tutor - Monitoring";
            this.getHistory()

        } else if (activeElement === "reflecting") {
            document.title = "AI Tutor - Reflecting";
            this.getHistory()

        } else if (activeElement == "tips") {
            this.updateNextPhaseStatus()
            window.location.href = "/chatgpt/tips";
            return;
        } else {
            localStorage.setItem("activeElement", "planning");
            document.title = "AI Tutor - Planning";
            this.getHistory()
            return;
        }

        this.scrollToBottom();
    }

    addPromptAnswer(prompt, answer) {
        const parent = document.getElementsByClassName("messages")[0];
        if (prompt && prompt.trim() !== "") {
            parent.appendChild(this.addPrompt(prompt));
        }

        parent.appendChild(this.addAnswer(answer));
    }

    addPrompt(message) {
        const prompt = document.createElement("p");
        prompt.className = "prompt";
        prompt.innerText = message;
        return prompt;
    }

    addAnswer(message) {
        var md = window.markdownit();
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
        var html = md.render(message);
        text.innerHTML = html.replace(/(\d+\.)/g, "<br>$1")
            .replace(/(<br>\d+\.\s*<strong>.*?<\/strong>:)/g, '<br>$1<br>')
            .replace(/ - (.*?)(?=<br>|\n|$| -)/g, (match, p1) => {
                return `<ul><li>${p1.trim()}</li></ul>`;
            })
        answerContainer.appendChild(text);
        return answerContainer;

    }

    scrollToBottom() {
        window.scrollTo(0, document.body.scrollHeight);
    }

    async getHistory() {
        try {
            const parent = document.getElementsByClassName("messages")[0];
            parent.innerHTML = ''
            const response = await fetch("/chatgpt/history", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ conversation_type: localStorage.getItem("activeElement") }),
            });

            const data = await response.json();

            if (data?.reply) {
                for (let i = 0; i < data.reply.length; i++) {
                    this.addPromptAnswer(data.reply[i].prompt, data.reply[i].reply);
                }
                localStorage.setItem('allowPlanningPhase', data?.allow_planning_phase)
                localStorage.setItem('allowMonitoringPhase', data?.allow_monitoring_phase)
                localStorage.setItem('allowReflectionPhase', data?.allow_reflection_phase)
                this.updatePhaseButtonState()
            } else {
                alert(data.error || "Error processing your message.");
            }
        } catch (error) {
            console.log(error);
            alert("An error occurred while communicating with the server.");
        }
        document.getElementById("prompt").value = "";
        this.scrollToBottom();
    }

    async updateNextPhaseStatus() {
        try {
            let currentActiveElement = localStorage.getItem("activeElement");
            const response = await fetch("/chatgpt/allow-next-phase", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ conversation_type: currentActiveElement }),
            });
            const data = await response.json();
            localStorage.setItem('allowPlanningPhase', data?.allow_planning_phase)
            localStorage.setItem('allowMonitoringPhase', data?.allow_monitoring_phase)
            localStorage.setItem('allowReflectionPhase', data?.allow_reflection_phase)

            this.updatePhaseButtonState()
    } catch(error) {
        console.log(error);
        alert("An error occurred while communicating with the server.");
    }
}

updatePhaseButtonState() {
    let monitoringButton = document.getElementById('monitoring');
    let reflectionButton = document.getElementById('reflecting');
    let planningButton = document.getElementById('planning');
    if (monitoringButton) {
        monitoringButton.disabled = localStorage.getItem("allowMonitoringPhase")
            ? localStorage.getItem("allowMonitoringPhase") !== "true"
            : false;

        if (monitoringButton.disabled) {
            monitoringButton.classList.add("off");
        } else {
            monitoringButton.classList.remove("off");
        }
    } else {
        console.error("monitoringButton not found in the DOM");
    }

    if (reflectionButton) {
        reflectionButton.disabled = localStorage.getItem("allowReflectionPhase")
            ? localStorage.getItem("allowReflectionPhase") !== "true"
            : false;


        if (reflectionButton.disabled) {
            reflectionButton.classList.add("off");
        } else {
            reflectionButton.classList.remove("off");
        }
    } else {
        console.error("reflectionButton not found in the DOM");
    }


    if (planningButton) {
        planningButton.disabled = localStorage.getItem("allowPlanningPhase")
            ? localStorage.getItem("allowPlanningPhase") !== "true"
            : false;


        if (planningButton.disabled) {
            planningButton.classList.add("off");
        } else {
            planningButton.classList.remove("off");
        }
    } else {
        console.error("planningButton not found in the DOM");
    }
}

}


export default LoadData;
