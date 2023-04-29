const fileName = document.querySelector(".fileName");
const form = document.querySelector('form');
const trainBtn = document.querySelector('#train-btn');
const predictBtn = document.querySelector('#predict-btn');
const output = document.querySelector('#output');
const predict = document.querySelector('#predict');
const fileInput = document.querySelector("input[type=file]");


fileInput.addEventListener("change", function() {
    if (this.files && this.files[0]) {
        fileName.innerHTML = this.files[0].name;
    }
});


// trainBtn.addEventListener('click', async() => {
//     output.innerHTML = 'Training...';
//     const response = await fetch('/train/');
//     const result = await response.text();
//     output.innerHTML = "Successfully,Training completed !!";
// });

// predictBtn.addEventListener('click', async() => {
//     predict.innerHTML = 'Predicting...';
//     const formData = new FormData(form);
//     const response = await fetch('/predict', {
//         method: 'POST',
//         body: formData
//     });
//     const result = await response.text();
//     predict.innerHTML = "Prediction completed ! Check the results !!";
// });

function submitForm() {
    var form = $('form')[0];
    var formData = new FormData(form);
    var action = $('select[name="action"]').val();
    $.ajax({
        url: '/' + action,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $('#result').html('<a href="' + response + '">Download</a>');
        }
    });
}