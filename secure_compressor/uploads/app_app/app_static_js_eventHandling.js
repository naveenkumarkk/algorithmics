import LoadData from "./LoadData.js";
import ClickEvents from "./ClickEvents.js";
import PromptHandling from "./PromptHandling.js";

const loadDataFromBackend = new LoadData();
const click = new ClickEvents();
const promptHandling = new PromptHandling();

const staticMessages = {
  planning:
    "This is a Planning Phase, here the AI Tutor helps you set clear goals and deadlines, encouraging you to create your own study plan for better self-regulation.",
  monitoring:
    "This is a Monitoring Phase, here the AI Tutor focuses on boosting motivation and keeping you on track with your study goals. Adjust as needed!",
  reflecting:
    "This is a Reflecting Phase, here, the AI Tutor helps you analyze your performance, identify improvements, and prepare for better outcomes.",
};

// Update static content dynamically
function updateStaticContent(phase) {
    const staticContent = document.getElementById("staticContent");
    if (staticContent && staticMessages[phase]) {
        staticContent.innerHTML = `<p>${staticMessages[phase]}</p>`;
    }
}

function clickPlanning(event) {
  click.clickPlanning();
  updateStaticContent("planning");

  loadDataFromBackend.clear();
  loadDataFromBackend.loadData();
}

function clickMonitoring(event) {
  click.clickMonitoring();
  updateStaticContent("monitoring");

  loadDataFromBackend.clear();
  loadDataFromBackend.loadData();
}

function clickReflecting(event) {
  click.clickReflecting();
  updateStaticContent("reflecting");

  loadDataFromBackend.clear();
  loadDataFromBackend.loadData();
}

function clickTips(event) {
  click.clickTips();
}

function submitForm(event) {
  event.preventDefault();

  const form = document.getElementById("promptInput");
  const prompt = new FormData(form).get("prompt");

  const keywords = ["completed", "finished", "done"];
  const isPhaseCompleted = keywords.some(keyword => prompt.toLowerCase().includes(keyword));

  promptHandling.handlePrompt(prompt);

  if (isPhaseCompleted) {
    form.classList.add("hidden");
  }

  form.reset();
}

document.getElementById("planning").addEventListener("click", clickPlanning);
document.getElementById("monitoring").addEventListener("click", clickMonitoring);
document.getElementById("reflecting").addEventListener("click", clickReflecting);
document.getElementById("tips").addEventListener("click", clickTips);
document.getElementById("promptInput").addEventListener("submit", submitForm);
document.addEventListener("keydown", (event) => {
  if (
    event.key === "Enter" &&
    (event.metaKey || event.ctrlKey) &&
    document.getElementById("prompt").value.trim() !== ""
  ) {
    submitForm(event);
  }
});

document.addEventListener("DOMContentLoaded", () => {
  // Set default static content to "Planning Phase"
  updateStaticContent("planning");
});
