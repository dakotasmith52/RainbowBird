const realFileButton = document.getElementById("real-file");
            const customButton = document.getElementById("custom-button");
            const customText = document.getElementById("custom-text");

            customButton.addEventListener("click", function() {
                realFileButton.click()
            });

            realFileButton.addEventListener("change", function() {
                if (realFileButton.value) {
                    customText.innerHTML = realFileButton.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
                } else {
                    customText.innerHTML = "No File Chosen"
                }
            });