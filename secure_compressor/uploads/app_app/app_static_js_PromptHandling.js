import LoadData from "./LoadData.js";
const loadData = new LoadData();

class PromptHandling {

  async handlePrompt(prompt) {
    try {
      const response = await fetch("/chatgpt/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: prompt, conversation_type: localStorage.getItem("activeElement") }),
      });

      const data = await response.json();
      
      if (data?.reply) {
        loadData.addPromptAnswer(prompt,data?.reply)
        localStorage.setItem('allowPlanningPhase',data?.allow_planning_phase)
        localStorage.setItem('allowMonitoringPhase',data?.allow_monitoring_phase)
        localStorage.setItem('allowReflectionPhase',data?.allow_reflection_phase)
        loadData.updatePhaseButtonState()

      } else {
        alert(data.error || "Error processing your message.");
      }
    } catch (error) {
      console.log(error);
      alert("An error occurred while communicating with the server.");
    }
    document.getElementById("prompt").value = "";
    loadData.scrollToBottom();
  }

}

export default PromptHandling;