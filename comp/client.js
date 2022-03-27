let join_button = document.getElementById("join");
let send_button = document.getElementById("send");
join_button.addEventListener("click", join_lobby);
send_button.addEventListener("click", send_message);

let ws = new WebSocket("ws://localhost:8004");
let started = false;

ws.onopen = function() {
    //alert("Connected to websocket");
}
ws.onmessage = function(event) {
    let message = JSON.parse(event.data)
    if (message.event === "message") {
        alert(message.data);
    }
    else if (message.event === "start") {
        alert("Game starting.");
        started = true;
        join_button.remove();
        send_button.remove();
    }
    else if (message.event === "question") {
        question = message.message;
        options = message.options;
        id = message.id;
        
        let q = document.createElement("p");
        q.innerHTML = question;
        q.className = id.toString();
        document.body.append(q);

        for (let op of options) {
            let option = document.createElement("button");
            option.className = id.toString();
            option.innerHTML = op;
            option.addEventListener("click", () => {
                answer_question(id, op);
            })
            document.body.append(option);
        }
    }
}
ws.onclose = function() {
    //alert("Connection closed");
}

function join_lobby() {
    ws.send("JOIN");
}
function send_message() {
    ws.send("PING");
}
function answer_question(qid, answer) {

    ws.send(JSON.stringify({
        event: "answer",
        qid: qid,
        choice: answer
    }));

    let related = document.getElementsByClassName(qid.toString());
    console.log(related);
    while (related[0]) {
        related[0].parentNode.removeChild(related[0]);
    }
}
