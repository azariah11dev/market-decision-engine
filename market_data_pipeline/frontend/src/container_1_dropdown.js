document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#container-1-dropdown-btn").onclick = () => {
        document.querySelector(".container-1-dropdown").classList.toggle("show");
    };
});