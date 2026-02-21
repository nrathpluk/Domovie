window.addEventListener("load", () => {
  document.querySelectorAll(".fade").forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight) {
      el.classList.add("show");
    }
  });
});
