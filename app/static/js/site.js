// Sidebar Menu Toggle
document.getElementById("menu-toggle").addEventListener("click", toggleMenu);

function toggleMenu() {
    var wrapper = document.getElementById("wrapper");
    wrapper.classList.toggle("toggled");
    window.dispatchEvent(new Event('resize'));
}

function SelectAllCheckboxes(source) {
    checkboxes = document.getElementsByName('network_checkbox');    
    for (var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = true;
    }
}

function ToggleLoadingAnimation() {
    var loadingAnimation = document.getElementById("loading-animation");
    var loadingText = document.getElementById("loading-animation-text");
    loadingAnimation.classList.remove("d-none");
    loadingText.classList.remove("d-none");    
}