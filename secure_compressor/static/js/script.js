document.getElementById("zipToggle").addEventListener("click", () => {
    document.getElementById("zipToggle").classList.add("active");
    document.getElementById("unzipToggle").classList.remove("active");
    document.getElementById("formTitle").textContent = "SecureCompressor - Zip File";
    document.getElementById("zipForm").classList.remove("hidden");
    document.getElementById("unzipForm").classList.add("hidden");
    clearOutput();
});

document.getElementById("unzipToggle").addEventListener("click", () => {
    document.getElementById("unzipToggle").classList.add("active");
    document.getElementById("zipToggle").classList.remove("active");
    document.getElementById("formTitle").textContent = "SecureCompressor - Unzip File";
    document.getElementById("unzipForm").classList.remove("hidden");
    document.getElementById("zipForm").classList.add("hidden");
    clearOutput();
});

document.getElementById("compressButton").addEventListener("click", () => {
    const files = document.getElementById("fileInput").files;
    const password = document.getElementById("passwordZip").value;

    if (!files.length || !password) {
        displayOutput("Please select files and enter a password.");
        return;
    }

    const formData = new FormData();
    Array.from(files).forEach(file => formData.append("files", file));
    formData.append("password", password);


    fetch("/compress", {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                displayOutput(data.error);
            } else {
                const downloadLink = `<a href="/download/${data.output}" target="_blank">Download Compressed File</a>`;
                displayOutput(`Files encrypted successfully. ${downloadLink}`);
            }
        })
        .catch(error => displayOutput(`Error: ${error}`));


    
});

document.getElementById("decompressButton").addEventListener("click", () => {
    const file = document.getElementById("zipFileInput").files[0];
    const password = document.getElementById("passwordUnzip").value;

    if (!file || !password) {
        displayOutput("Please select a valid ZIP file and enter a password.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("password", password);

    fetch("/decompress", {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                displayOutput(data.error);
            } else {
                const downloadUrl = `/download/${data.output}`;
                const downloadButton = `<button onclick="downloadFile('${downloadUrl}', '${data.output.split('/').pop()}')">Download Folder</button>`;
                displayOutput(`Files decrypted successfully. ${downloadButton}`);
            }
        })
        .catch(error => displayOutput(`Error: ${error}`));    
});

function displayOutput(message) {
    const outputDiv = document.getElementById("output");
    outputDiv.innerHTML = message;
}

function clearOutput() {
    const outputDiv = document.getElementById("output");
    outputDiv.textContent = "";
}

function downloadFile(url, filename) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok.");
            }
            return response.blob();
        })
        .then(blob => {
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = filename; // Suggested filename
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(error => {
            console.error("Download error:", error);
            alert("Failed to download the file.");
        });
}

