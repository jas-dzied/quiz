let ws = new WebSocket("ws://82.35.235.223:42069");

function delete_class(id) {
    var paras = document.getElementsByClassName(id);
    while(paras[0]) {
        paras[0].parentNode.removeChild(paras[0]);
    }
}
function gen_element(tag) {
    let element = document.createElement(tag);
    document.body.appendChild(element);
    return element;
}
function create_text(text, id) {
    let element = gen_element("p");
    element.innerHTML = text;
    element.className = id;
}

ws.onopen = function() {
}

ws.onmessage = function(event) {
    let message = JSON.parse(event.data)
    if (message.event == "host") {
        let start = gen_element("button");
        start.innerHTML = "start game";
        start.className = 1
        start.addEventListener("click", () => {
            ws.send(JSON.stringify({
                event: "start"
            }))
        })
        create_text("You are the host.", 1);
        create_text("Players:", 1);
    } else if (message.event == "player_joined") {
        create_text(message.username, 1);
    } else if (message.event == "host_question") {
        let end = gen_element("button");
        end.innerHTML = "next question";
        end.className = 2;
        end.addEventListener("click", () => {
            ws.send(JSON.stringify({
                event: "next_question"
            }));
            delete_class(2);
        })
        create_text("Players that have answered:", 2);
    } else if (message.event == "player_answered") {
        create_text(message.username, 2);
    } else if (message.event == "request_username") {
        create_text("What is your username?", 1);
        let input = gen_element("input");
        input.className = 1;
        let confirm = gen_element("button");
        confirm.innerHTML = "join game"
        confirm.className = 1;
        confirm.addEventListener("click", () => {
            if (input.value != "") {
                ws.send(JSON.stringify({
                    event: "username",
                    username: input.value
                }));
                delete_class(1);
                create_text("Joined successfully. Waiting for host to start.", 1);
            }
        })
    } else if (message.event == "delete_class") {
        delete_class(message.cls);
    } else if (message.event == "question") {
        delete_class(2)
        create_text(message.text, 2)
        message.options.map((option) => {
            let button = gen_element("button");
            button.innerHTML = option;
            button.className = 2;
            button.addEventListener("click", () => {
                ws.send(JSON.stringify({
                    event: "answer",
                    choice: option
                }));
                delete_class(2);
                create_text("Waiting for host to start the next question.", 2);
            })
        })
    } else if (message.event == "end") {
        create_text("Game over.", 2);
    } else if (message.event == "leaderboard") {
        delete_class(2);
        create_text("Leaderboard:", 2)
        Object.keys(message.players).forEach(user => {
            create_text(user+": "+message.players[user].toString(), 2);
        })
    }
}

ws.onclose = function() {
}
