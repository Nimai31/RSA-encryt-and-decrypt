function encrypt() {
    var userInput = document.getElementById('encrypt-message').value;
    try {
        fetch('/encrypt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'encrypt_message=' + encodeURIComponent(userInput),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = "Encrypted data: " + data.result.join(' ');
        })
        .catch(error => {
            alert("Encryption failed: " + error);
        });
    } catch (error) {
        alert("Encryption failed: " + error);
    }
}

function decrypt() {
    var userInput = document.getElementById('decrypt-message').value;
    try {
        fetch('/decrypt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'decrypt_message=' + encodeURIComponent(userInput),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = "Decrypted message: " + data.result;
        })
        .catch(error => {
            alert("Decryption failed: " + error);
        });
    } catch (error) {
        alert("Decryption failed: " + error);
    }
}
