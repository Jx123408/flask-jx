<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>整理券発行</title>
</head>
<body>
    <h1>演劇祭 整理券発行</h1>
    <p>残りの整理券: <span id="remaining">{{ remaining }}</span></p>

    <form id="ticketForm">
        <label>お名前: <input type="text" name="name" required></label><br>
        <label>公演名: <input type="text" name="event" required></label><br>
        <button type="submit">整理券を発行</button>
    </form>

    <div id="ticketInfo" style="display: none;">
        <h2>発行された整理券</h2>
        <p>整理券番号: <span id="ticketId"></span></p>
        <img id="qrCode" src="" alt="QRコード">
    </div>

    <script>
        document.getElementById("ticketForm").addEventListener("submit", function(event) {
            event.preventDefault();
            const formData = new FormData(this);

            fetch("/issue", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                document.getElementById("ticketId").innerText = data.ticket_id;
                document.getElementById("qrCode").src = "/qr/" + data.ticket_id;
                document.getElementById("ticketInfo").style.display = "block";
            })
            .catch(error => console.error("Error:", error));
        });
    </script>
</body>
</html>
