document.addEventListener("DOMContentLoaded", function() {
    const dateInput = document.getElementById("date");
    if (dateInput) {
        // Set default date to today
        const today = new Date().toISOString().split("T")[0];
        dateInput.setAttribute("min", today);
        dateInput.value = today;
    }
});
