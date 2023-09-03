let webcamStarted = false;
let webcamStream = null;
let predictionInterval = null;

function startWebcam() {
    if (!webcamStarted) {
        webcamStarted = true;

        const video = document.createElement('video');
        document.getElementById('webcam-container').appendChild(video);

        const imagePredictionDiv = document.getElementById('image-prediction');
        if (imagePredictionDiv) {
            imagePredictionDiv.remove();
        }

        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
            webcamStream = stream;
            video.srcObject = stream;
            video.play();
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;

            // Every 1 second, send a frame to the server to get a prediction
            predictionInterval = setInterval(() => {
                sendFrameToServer(video);
            }, 1000);
        });
    }
}

function stopWebcam() {
    if (webcamStarted) {
        webcamStarted = false;

        if (webcamStream) {
            webcamStream.getTracks().forEach(track => track.stop());
        }

        clearInterval(predictionInterval);
        predictionInterval = null;

        const videoElement = document.querySelector('video');
        if (videoElement) {
            videoElement.pause();
            videoElement.srcObject = null;
            videoElement.remove();
        }

        const displayDiv = document.getElementById('webcam-prediction');
        displayDiv.innerHTML = '';

        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
    }
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
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
    })
        .then(response => response.json())
        .then(data => {
            const displayDiv = document.getElementById('webcam-prediction');
            displayDiv.innerHTML = `
    <h3 class="text-light mt-3 p-5">
      ${data.label} with confidence: ${data.confidence.toFixed(2)}
    </h3>  
            `;
        });
}

function clearUploadedPrediction() {
    const imagePredictionDiv = document.getElementById('image-prediction');
    if (imagePredictionDiv) {
        imagePredictionDiv.remove();
    }
}
