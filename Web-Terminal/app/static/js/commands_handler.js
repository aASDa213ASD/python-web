// commands.js
const valid_folders = ["/", "about", "gamehacking", "gallery", "system", "whoami", "feedback", "todo"];
const valid_commands = ["skills", "whoami", "exit", "cookies", "feedback", "todo", "register", "users"];

function update_caret_position() {
    const textarea = document.getElementById('command_input');
    const caret = document.getElementById('custom_caret');

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

function clear_terminal() {
    const initial_message = document.getElementById("initial_message");
    const output = document.getElementById("command_output");

    try { initial_message.innerHTML = ""; } 
    catch (error) {}

    try { output.innerHTML = ""; } 
    catch (error) {}
}

async function fetch_async(route) {
    const response = await fetch(route);
    const text = await response.text();
    const output = document.getElementById("command_output");
    output.innerHTML = output.innerHTML + text;
}

function throw_invalid_route(route) {
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

function throw_invalid_user(username) {
    const text = "<p class='text-description'>User <span class='text-important'>'" + username + "'</span> does not exist</p>";
    const output = document.getElementById("command_output");
    output.innerHTML = output.innerHTML + text;
}

function display_auth_failure() {
    const text = "<p class='text-description'>Authentication failure</p>";
    const output = document.getElementById("command_output");
    output.innerHTML = output.innerHTML + text;
}

function display_user_credentials(username) {
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
                throw_invalid_user(username);
        })
        .catch(error => console.error('Error fetching JSON file:', error));
}

function validate_credentials(username, password) {
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
                throw_invalid_route(cmd[1]);
            break;
        case "ls":
            fetch_async("/ls");
            break;
        case "help":
            fetch_async("/help");
            break;
        case "clear":
            clear_terminal();
            break;
        case "whois":
            fetch_async("/whois");
            break;
        case "projects":
            fetch_async("/projects");
            break;
        case "passwd":
            if (cmd.length == 1)
                submitForm = true;
            else if (cmd.length == 3)
                submitForm = true;
            else if (cmd.length == 2)
                display_user_credentials(cmd[1].trim());
            else
                throw_invalid_user(cmd[1]);
            break;
        case "login":
            if (cmd.length >= 3) {
                await validate_credentials(cmd[1].trim(), cmd[2].trim())
                    .then(isValid => {
                        if (isValid)
                            submitForm = true;
                        else
                            display_auth_failure();
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

    update_caret_position();
}

function handle_enter_command(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("shell").dispatchEvent(new Event("submit"));
    }
}
