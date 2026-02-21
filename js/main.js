// fade on load
window.addEventListener("load", () => {
  document.querySelectorAll(".fade").forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight) {
      el.classList.add("show");
    }
  });
});

const cards = document.querySelectorAll(".movie-item");

// overlay
const overlay = document.createElement("div");
overlay.className = "zoom-overlay";
document.body.appendChild(overlay);

cards.forEach(card => {
  card.addEventListener("click", () => {
    const rect = card.getBoundingClientRect();
    const link = card.dataset.link;
    const scale = 2.2;

    // clone การ์ด
    const clone = card.cloneNode(true);
    clone.classList.add("zoom-netflix");

    // ซ่อนตัวจริง
    card.style.visibility = "hidden";

    // วาง clone ตำแหน่งเดิม
    clone.style.position = "fixed";
    clone.style.top = rect.top + "px";
    clone.style.left = rect.left + "px";
    clone.style.width = rect.width + "px";
    clone.style.height = rect.height + "px";
    clone.style.margin = 0;

    document.body.appendChild(clone);
    overlay.style.display = "block";

    clone.getBoundingClientRect();

    // ย้ายไปกลางจอ + zoom
    clone.style.top = "50%";
    clone.style.left = "50%";
    clone.style.transform = `translate(-50%, -50%) scale(${scale})`;

    // ไปหน้าถัดไป
    setTimeout(() => {
      window.location.href = link;
    }, 900);
  });
});

