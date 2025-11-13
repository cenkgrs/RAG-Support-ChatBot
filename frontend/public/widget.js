(function () {
    const script = document.currentScript;
    const bg = script.dataset.bg || "#ffffff";
    const header = script.dataset.header || "Sohbet Et";
    const botId = script.dataset.botId;
    const logo = script.dataset.logo;

    // Chat container oluştur
    const container = document.createElement("div");
    container.className = "chat-widget-container";
    container.style.position = "fixed";
    container.style.bottom = "20px";
    container.style.right = "20px";
    container.style.zIndex = "9999";
    container.style.width = "360px";
    container.style.minHeight = "60vh";
    container.style.border = "none";
    container.style.display = "none";
    container.style.display = "rgba(255, 255, 255, 0.9)";
    container.style.backdropFilter = "blur(15px)";
    container.style.borderRadius = "20px";
    container.style.boxShadow = "0 8px 24px rgba(0, 0, 0, 0.15)";
    // container.style.display = "flex";
    container.style.flexDirection = "column";
    container.style.overflow = "hidden";
    container.style.animation = "fadeIn 0.3s ease";
    container.style.background = "white";


    // iframe oluştur
    const iframe = document.createElement("iframe");
    iframe.src = `http://localhost:5173/chat.html?bot=${botId}&bg=${encodeURIComponent(bg)}&header=${encodeURIComponent(header)}&logo=${encodeURIComponent(logo)}`;
    iframe.style.width = "100%";
    iframe.style.height = "65vh";
    iframe.style.border = "none";
    iframe.style.borderRadius = "12px";
    container.appendChild(iframe);

    // Chat aç/kapa butonu
    const toggleBtn = document.createElement("button");
    toggleBtn.innerHTML = "<img src='http://localhost:5173/argedestek.png'/>";
    toggleBtn.style.position = "fixed";
    toggleBtn.style.bottom = "20px";
    toggleBtn.style.right = "20px";
    toggleBtn.style.background = "white";
    toggleBtn.style.color = "white";
    toggleBtn.style.border = "1px solid #e5e5e5";
    toggleBtn.style.borderRadius = "50%";
    toggleBtn.style.width = "75px";
    toggleBtn.style.minHeight = "75px";
    toggleBtn.style.cursor = "pointer";
    toggleBtn.style.zIndex = "10000";
    toggleBtn.style.boxShadow = "0 0 4px 1px #E5E5E5";
    toggleBtn.style.padding = "10px";

    toggleBtn.onclick = () => {
        container.style.display = container.style.display === "none" ? "block" : "none";
        toggleBtn.style.display = container.style.display === "none" ? "block" : "none";
    };

    document.body.appendChild(toggleBtn);
    document.body.appendChild(container);

    window.addEventListener('message', (event) => {
        if (event.data.type === 'CLOSE_CHAT_WIDGET') {
            container.style.display = 'none';
            toggleBtn.style.display = "block";
        }
    });
})();
