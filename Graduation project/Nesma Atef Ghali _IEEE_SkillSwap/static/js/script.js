// ==================== Small UI Helpers ====================
document.addEventListener("DOMContentLoaded", () => {
    const flashes = document.querySelectorAll(".flash");
    setTimeout(() => flashes.forEach((flash) => {
        flash.style.opacity = "0";
        setTimeout(() => flash.remove(), 300);
    }), 3500);
});

function showDemoMessage() {
    alert("This is a demo profile. Create another real SkillSwap account to test a real swap request.");
}
