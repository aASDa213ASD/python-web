// commands.js
const valid_folders = ["/", "about", "gamehacking", "gallery", "system", "skills", "whoami", "login"];
const valid_commands = ["system", "skills", "whoami", "exit", "cookies"];

function updateCaretPosition() {
    const textarea = document.getElementById('commandInput');
    const caret = document.getElementById('customCaret');

    const textWidth = getTextWidth(textarea.value, window.getComputedStyle(textarea).font);
    const textareaRect = textarea.getBoundingClientRect();

    caret.style.left = (textWidth + textareaRect.left - 40) + 'px'; // Adjust 5 pixels for better alignment
}

function getTextWidth(text, font) {
    const canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement("canvas"));
    const context = canvas.getContext("2d");
    context.font = font;
    const metrics = context.measureText(text);
    return metrics.width;
}

function clearConsole() {
    const initial_message = document.getElementById("initial_message");
    const output = document.getElementById("command_output");

    try { initial_message.innerHTML = ""; } 
    catch (error) {}

    try { output.innerHTML = ""; } 
    catch (error) {}
}

async function asyncFetch(route) {
    const response = await fetch(route);
    const text = await response.text();
    const output = document.getElementById("command_output");
    output.innerHTML = output.innerHTML + text;
}

function showInvalidRoute(route) {
    const text = "<p class='text-description'>Route '" + route + "' does not exist</p>";
    const output = document.getElementById("command_output");
    output.innerHTML = output.innerHTML + text;
}

function showCommandNotFound(command) {
    if (command === '') 
        return;
    
    const output = document.getElementById("command_output");
    const text = "<div><p class='text-description'>Command <span class=text-command>'" + command + "'</span> not found. For a list of commands, type <span class='text-command'>'help'</span></p></div>";
    output.innerHTML = output.innerHTML + text;
}

function showInvalidUser(username) {
    const text = "<p class='text-description'>User <span class='text-important'>'" + username + "'</span> does not exist</p>";
    const output = document.getElementById("command_output");
    output.innerHTML = output.innerHTML + text;
}

function showAuthenticationFailure() {
    const text = "<p class='text-description'>Authentication failure</p>";
    const output = document.getElementById("command_output");
    output.innerHTML = output.innerHTML + text;
}

function showUserCredentials(username) {
    const jsonFilePath = 'static/json/users.json';

    fetch(jsonFilePath)
        .then(response => response.json())
        .then(credentials => {
            const user = credentials.users.find(user => user.username === username);

            if (user) {
                const text = `<div>
                    <hr>
                    <pre><span class="text-description">User credentials <span class="text-important">ID:PWD</span></span></pre>
                    <pre><span class="text-important">${user.username}:${user.password}</span></pre>
                </div>`;

                const output = document.getElementById("command_output");
                output.innerHTML = output.innerHTML + text;
            } 
            else
                showInvalidUser(username);
        })
        .catch(error => console.error('Error fetching JSON file:', error));
}

function validateCredentials(username, password) {
    const jsonFilePath = 'static/json/users.json';

    return fetch(jsonFilePath)
        .then(response => response.json())
        .then(credentials => {
            const user = credentials.users.find(user => user.username === username && user.password === password);
            return Boolean(user);
        })
        .catch(error => {
            console.error('Error fetching JSON file:', error);
            return false;
        });
}

document.querySelector("form").onsubmit = async function(e) {
    const input = document.querySelector('textarea[name="command"]'); 
    const cmd = input.value.split(' ');

    submitForm = false;
    e.preventDefault();

    switch(cmd[0].toLowerCase()) {
        case "cd":
            if (cmd.length > 1 && valid_folders.includes(cmd[1].trim()) || cmd.length === 1)
                submitForm = true;
            else
                showInvalidRoute(cmd[1]);
            break;
        case "ls":
            asyncFetch("/ls");
            break;
        case "help":
            asyncFetch("/help");
            break;
        case "clear":
            clearConsole();
            break;
        case "whois":
            asyncFetch("/whois");
            break;
        case "projects":
            asyncFetch("/projects");
            break;
        case "passwd":
            if (cmd.length == 3)
                submitForm = true;
            else if (cmd.length == 2)
                showUserCredentials(cmd[1].trim());
            else
                showInvalidUser(cmd[1]);
            break;
        case "login":
            if (cmd.length >= 3) {
                await validateCredentials(cmd[1].trim(), cmd[2].trim())
                    .then(isValid => {
                        if (isValid)
                            submitForm = true;
                        else
                            showAuthenticationFailure();
                    })
                    .catch(error => {
                        console.error('Error validating credentials:', error.message);
                    });
            }
            else
                submitForm = true;
            break;
        default:
            if (!valid_commands.includes(cmd[0].trim()))
                showCommandNotFound(cmd[0])
            else
                submitForm = true;
    }

    if (submitForm) 
      e.target.submit()
    else
        input.value = "";

    updateCaretPosition();
}

function handleEnterCommand(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("shell").dispatchEvent(new Event("submit"));
    }
}
