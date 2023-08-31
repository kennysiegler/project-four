candlesticks = 'http://127.0.0.1:5000/api/candlestick'

d3.json(candlesticks).then(function(candlestick_data) {
    // console.log(candlestick_data)
        loadData(candlestick_data)
})
function loadData(data) {
    for (let i = 0; i < data.length; i++ ) {
        const x = document.getElementById('selDataset')
        const y = document.createElement('option')
        y.setAttribute('id', data[i])
        y.setAttribute('value', data[i])
        y.innerText = data[i]
        x.appendChild(y)
        console.log(data[i])
    }   
    console.log(data)
}





