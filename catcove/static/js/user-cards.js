const user_profile = {
    "nickname": "小地瓜",
    "id": 1,
    "status": "normal",
    "role": "user",
    "avatar": "https://picx.zhimg.com/v2-773ff19db11925fdc57ad90dffc9e0a4_xll.jpg",
    "info": "啦啦啦",
};

class UserCard extends HTMLElement {
    constructor() {
        super();
        let shadow = this.attachShadow({ mode: "open" });
        // Fetch the user's info from class.
        // let user_json = document.getElementsByClassName("user-info-full");

        // Profile
        let profile = document.createElement("article");
        profile.classList = ["user-profile"];

        // Masthead
        let masthead = document.createElement("header"); // Change here
        masthead.classList = ["masthead"];

        // Avator.
        let userAvator = document.createElement("div");
        userAvator.classList = ["masthead-avater"];
        let userAvatorRaw = document.createElement("img");
        userAvatorRaw.classList = "user-avatar";
        userAvatorRaw.alt = "Avatar not uploaded.";
        userAvatorRaw.src = user_profile.avatar;

        // Nickname.
        let userNickname = document.createElement("hgroup");
        userNickname.innerHTML = "<h3>" + user_profile.nickname + "</h3>";
        userNickname.innerHTML += "<h4>" + user_profile.info + "</h4>";

        // Content in profile
        let info_body = document.createElement("body");
        info_body.classList = ["user-profile-body"];

        // Style
        var style = document.createElement("style");
        style.textContent = "/* Masthead */\n" + 
        ".masthead{" +
        "background-color: #394046;" + 
        "background-position: center; background-size: cover; border-radius: 16px;" +
        "background-image: url('https://picx.zhimg.com/80/v2-aa5d011f9276451e75d6be72131f0ade_r.jpg')" // May update.
        + "}\n" +
        ".masthead-avater{" + "width: 84px; height: 84px; border-radius: 45%; align-items: center;" +
        "overflow: hidden;" // Make it covered.
        + "}\n" +
        ".user-avatar{display: flex; width: 100%; height: 100%;}\n" +
        ".user-profile-body{}"

        userAvator.appendChild(userAvatorRaw);
        masthead.appendChild(userAvator);
        masthead.appendChild(userNickname);
        // shadow.appendChild(masthead);
        profile.appendChild(masthead);
        profile.appendChild(info_body);
        shadow.appendChild(profile);
        shadow.append(style);
    };
}

customElements.define('user-card', UserCard);