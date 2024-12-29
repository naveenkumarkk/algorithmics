class GeneralFunctions {
    toggleDarkmode() {
        if (localStorage.getItem("darkMode") === "enabled") {
            document.body.classList.add("dark-mode");
        }
    }
    googleAuthentication () {
        google.accounts.id.initialize({
            client_id: "545909832666-56nf3cpa8jau6o42p8f50pv99pv391pa.apps.googleusercontent.com",
            callback: this.handleCredentialResponse
        });

        google.accounts.id.renderButton(
            document.getElementById("g_id_signin"), 
            { theme: "outline", size: "large" } 
        );

        google.accounts.id.prompt();
    };

    handleCredentialResponse(response) {
        console.log("Encoded JWT ID token: " + response.credential);
        
    }
}

export default GeneralFunctions;