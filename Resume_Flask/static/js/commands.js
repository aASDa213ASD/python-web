// commands.js
const valid_folders = ["about", "test"];
const valid_commands = ["home"]

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
    initial_message.innerHTML = "";
    output.innerHTML = "";
}

async function asyncFetch(route) {
    const response = await fetch(route);
    const text = await response.text();
    const output = document.getElementById("command_output");
    output.innerHTML = output.innerHTML + text;
}

function showInvalidRoute(route) {
    const text = "<p>Error: Route '" + route + "' does not exist</p>";
    const output = document.getElementById("command_output");
    output.innerHTML = output.innerHTML + text;
}

function showCommandNotFound(command) {
    const text = "<div><p class='text-description'>Command '" + command + "' not found. For a list of commands, type <span class='text-command'>'help'</span></p></div>";
    const output = document.getElementById("command_output");
    output.innerHTML = output.innerHTML + text;
}

document.querySelector("form").onsubmit = function(e) {
    const input = document.querySelector('textarea[name="command"]'); 
    const cmd = input.value.split(' ');

    submitForm = false;
    e.preventDefault();

    switch(cmd[0]) {
        case "cd":
            if (cmd.length > 1 && cmd[1].trim() !== "" && valid_folders.includes(cmd[1].trim()))
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
