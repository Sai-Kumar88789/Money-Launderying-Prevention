const form = document.querySelector('form');
const trainBtn = document.querySelector('#train-btn');
const predictBtn = document.querySelector('#predict-btn');
const output = document.querySelector('#output');

form.addEventListener('submit', async(e) => {
    e.preventDefault();
    output.innerHTML = 'Loading...';

    const formData = new FormData(form);
    const response = await fetch('/uploadfile/', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();
    output.innerHTML = `Uploaded file: ${result.filename}`;
});

trainBtn.addEventListener('click', async() => {
    output.innerHTML = 'Training...';
    const response = await fetch('/train/');
    const result = await response.text();
    output.innerHTML = `Training complete: ${result}`;
});

predictBtn.addEventListener('click', async() => {
    output.innerHTML = 'Predicting...';
    const formData = new FormData(form);
    const response = await fetch('/predict/', {
        method: 'POST',
        body: formData
    });
    const result = await response.text();
    output.innerHTML = result;
});