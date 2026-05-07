const statusText = document.getElementById("status");

function setStatus(text) {
    statusText.innerText = text;
}

async function loadGreeting() {

    try {

        const response = await fetch("/greeting");

        const data = await response.json();

        setStatus(data.message);

        // start listening after greeting
        setTimeout(() => {
            startListening();
        }, 2000);

    } catch (error) {

        console.error(error);

        setStatus("Connection failed");
    }
}

async function startListening() {

    try {

        setStatus("Speak now...");

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        const mediaRecorder = new MediaRecorder(stream);

        const audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {

            setStatus("Uploading audio...");

            const audioBlob = new Blob(audioChunks, {
                type: "audio/webm"
            });

            const formData = new FormData();

            formData.append("audio", audioBlob, "recording.webm");

            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            console.log(data);

            // show AI response
            setStatus(data.response);

            // stop microphone
            stream.getTracks().forEach(track => track.stop());

            // play AI voice
            const audio = new Audio(data.audio_url);

            setStatus("EchoGuard is speaking...");

            await audio.play();

            // after AI finishes speaking
            audio.onended = () => {

                // restart conversation loop
                startListening();
            };
        };

        // give user preparation time
        setTimeout(() => {

            mediaRecorder.start();

            console.log("Recording started");

            setStatus("Listening...");

            // record for 6 seconds
            setTimeout(() => {

                mediaRecorder.stop();

            }, 6000);

        }, 1000);

    } catch (error) {

        console.error(error);

        setStatus("Microphone permission denied");
    }
}

loadGreeting();