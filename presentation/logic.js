results_url = 'http://127.0.0.1:5000/api/results'

let results_info = d3.json(results_url).then(function(results_data) {
    return results_data
})


function displayName() {

    results_info.then(function(d) {
        let sample_size = document.getElementById('sample_size')
        sample_size.innerText = "Sample Size: " + d['Training Sample Size']

        let model_type = document.getElementById('model_type')
        model_type.innerText = "Model Type: " + d['Model Type']
        
        let model_size = document.getElementById('model_size')
        model_size.innerText = "Model Size: " + d['Model Size']
        
        let training_precision = document.getElementById('training_precision')
        training_precision.innerText = "Training Precision: " + (d['Training Precision'] * 100).toFixed(2) +"%"
       
        let testing_precision = document.getElementById('testing_precision')
        testing_precision.innerText = "Testing Precision: " + (d['Testing Precision'] * 100).toFixed(2)+'%'

        let prediction = document.getElementById('prediction')
        if (d['Prediction'] == 1) {
            prediction.innerText = "Our Model Suggests that you buy tomorrow when the market opens and sell when it closes"
        } else if (d['Prediction'] == 0) {
            prediction.innerText = "Our Model Suggests that you should not buy tomorrow when the market opens and sell when it closes"
        } else {
            prediction.innerText = "We have an invalid variable in our Prediction field"
        }



    })
}



displayName()

