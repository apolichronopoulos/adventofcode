// List of random elements to prepend
const elements = [
    "$year={year};",
    "/*{year}*/",
    "//{year}",
    "/^{year}$/",
    "0.0.0.0:{year}",
    "0b1010|{year}",
    "0x0000|{year}",
    "0xffff&{year}",
    "<y>{year}</y>",
    "<{year}>|",
    "D-ONE|{year}",
    "int y={year};",
    "sub y{{year}}",
    "var y={year};",
    "y({year})",
    "{:year {year}}",
    "{year}",
];

// Function to update the year display dynamically
function updateYearDisplay() {
    // Get the current year dynamically
    const year = new Date().getFullYear();

    // Pick a random template from the list
    const randomTemplate = elements[Math.floor(Math.random() * elements.length)];

    // Replace {year} with a styled span
    const finalDisplay = randomTemplate.replace(
        "{year}",
        `<span class="highlight">${year}</span>`
    );

    // Display the final text in the #dynamic-year element
    const displayElement = document.getElementById("dynamic-year");
    displayElement.innerHTML = finalDisplay; // Use innerHTML to render HTML
}

// Call the function to initialize
updateYearDisplay();

// Optional: Refresh the display every 5 seconds
//setInterval(updateYearDisplay, 5000);
