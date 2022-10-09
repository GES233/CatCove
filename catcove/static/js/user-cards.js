const user_profile = {
    "nickname": "小地瓜",
    "id": 1,
    "avatar": "https://picx.zhimg.com/v2-773ff19db11925fdc57ad90dffc9e0a4_xll.jpg"
};
class UserCard extends HTMLElement {
    constructor() {
        super();
        let shadow = this.attachShadow({ mode: "open" });

        // Masthead
        let masthead = document.createElement("div");
        masthead.classList = ["masthead"];

        // Avator.
        let userAvator = document.createElement("div");
        userAvator.classList = ["masthead-avater"];
        let userAvatorRaw = document.createElement("img");
        userAvatorRaw.classList = "user-avatar";
        userAvatorRaw.alt = "";
        userAvatorRaw.src = user_profile.avatar;

        // Nickname.
        let userNickname = document.createElement("hgroup");
        userNickname.innerHTML = "<h1>" + user_profile.nickname + "</h1>";

        // Profile
        let profile = document.createElement("article");
        profile.classList = ["user-profile"];

        // Style
        var style = document.createElement("style");
        style.textContent = "/* Masthead */\n" + 
        ".masthead{" +
        "background-color: #394046; background-position: center; background-size: cover;" +
        "background-image: url('https://picx.zhimg.com/80/v2-aa5d011f9276451e75d6be72131f0ade_r.jpg')" +
        "}\n" +
        ".masthead-avater{" + "width: 84px;  height: 84px;  border-radius: 50%;" +
        "overflow: hidden;" // Make it covered.
        + "}\n" +
        ".user-avatar{display: flex; width: 100%; height: 100%}\n" 

        userAvator.appendChild(userAvatorRaw);
        masthead.appendChild(userAvator);
        masthead.appendChild(userNickname);
        shadow.appendChild(masthead);
        shadow.appendChild(profile);
        shadow.append(style);
    };
}

customElements.define('user-card', UserCard);