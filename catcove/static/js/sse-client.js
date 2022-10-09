function sse() {
    var status = "off";
    var source = new EventSource("/subscribe", { withCredentials: true });

    source.onopen = function (event) {
        console.log("[SSE]: SSE Started...");
        console.log("Ping from client.");
        status = "on"
    }
    // For `event: site`
    source.addEventListener("site", (event) => {
        window.console.log(`${event.data} from server.`);
    })
    // Ping from client.
    // Pong from server.

    // For `event: close`.
    source.addEventListener("close", (event) => {
        console.log("[SSE]: Close SSE...");
        source.close();
        status = "off"
    })
    // For `event: message`
    source.addEventListener("message", (event) => {
        const type = event.type;
        window.console.log(`Data:\r\n${event.data}\r\nWith type: ${type}`);
    })

    return source;
}


var message_loc = document.getElementById("message");
var source = sse();

const catCoveSSE = {
    // Config.
    _sseStatus: "off",
    sourceUrl: "/subscribe",
    abstractInfoTarget: "#message",
    interactionTarget: "#intrc",
    markTarget: "#mark",
    siteMessageTarget: "#site",

    // Init.
    init () {},

    // Get message from sse.
    linstenFromPublisher() {
        // Only a loop.
    },

    // Parse and render message.
    updateMessage(type, item) {
        var messageNode = document.querySelector(this.abstractInfoTarget);
    },
}
