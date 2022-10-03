function sse() {
    var source = new EventSource("/subscribe", { withCredentials: true });

    source.onopen = function (event) {
        console.log("[SSE]: SSE Started...");
    }

    var disconn_num = 0
    source.onerror = function (event) {
        disconn_num += 1;
        console.log("[SSE]: Disconnect to '/subcribe'.");
        if (disconn_num > 5) {
            console.log("[SSE]: Close SSE Connection.");
            alert("SEE not enabled");
            source.close();
        }
    }
    source.onmessage = function (event) {
        // Data.
        data = event.data
    }

    return source;
}

// 关于信息推送的部分
/*
<div id="message">
    <details role="list" dir="rtl">
    <summary aria-haspopup="listbox" role="link"><a href="#", onclick="toggleServer()"></a></summary>
    </details>
</div>
*/
var message_loc = document.getElementById("message");
var source = sse();

function toggleInfoPush() {
    if (source.CLOSED) {
        alert("服务器端未支持 Server-send event 。");
    }
    else {
        // Set server's status to get have supperly.
        var current_client_state = null
        if (current_client_state == "手动获取") {
        } else {
            //
        }
    }
}
