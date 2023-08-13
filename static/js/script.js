function startWebcam() {
    // Access the webcam and display it
    const video = document.createElement('video');
    document.getElementById('webcam-container').appendChild(video);
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.play();
            // Every 1 second, send a frame to the server to get a prediction
            setInterval(() => {
                sendFrameToServer(video);
            }, 1000);
        });
}

function sendFrameToServer(video) {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const imageData = canvas.toDataURL('image/jpeg').split(',')[1];
    fetch('/predict-webcam', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        const displayDiv = document.getElementById('webcam-prediction');
        displayDiv.innerHTML = `Predicted Brand: ${data.label} with confidence: ${data.confidence.toFixed(2)}`;
    });
}
