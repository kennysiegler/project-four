candlesticks = 'http://127.0.0.1:5000/api/candlestick'
backtest = 'http://127.0.0.1:5000/api/backtest'


let backtest_info = d3.json(backtest).then(function(backtest_data) {
    loadBacktestData(backtest_data)

})


d3.json(candlesticks).then(function(candlestick_data) {
    // console.log(candlestick_data)
        loadData(candlestick_data)
})
function loadData(data) {
    for (i in data) {
        const x = document.getElementById('selDataset')
        const y = document.createElement('option')
        y.setAttribute('id', i)
        y.setAttribute('value', i)
        y.innerText = i
        x.appendChild(y)
        
    }   
    
}

function yearSelected(year) {

    d3.json(candlesticks).then(function(data) {
        console.log()
        
        first_day = data[year]['dates'][0]
        last_day = data[year]['dates'][data[year]['dates'].length-1]
        console.log(first_day, last_day)
        var trace1 = {
            x: data[year]['dates'],
            close: data[year]['close'],
            high: data[year]['high'],
            open: data[year]['open'],
            low: data[year]['low'],
            type: 'candlestick',
            xaxis: 'x',
            yaxis: 'y'


        };

        var data = [trace1];

        var layout = {
            dragmode: 'zoom', 
            margin: {
              r: 10, 
              t: 25, 
              b: 40, 
              l: 60
            }, 
            showlegend: false, 
            xaxis: {
              autorange: true, 
              domain: [0, 1], 
              range: [ first_day, last_day ], 
              rangeslider: {range: [first_day, last_day]}, 
              title: 'Date', 
              type: 'date'
            }, 
            yaxis: {
              autorange: true, 
              domain: [0, 1], 
              range: [100, 150], 
              type: 'linear'
            }
          };
          
          Plotly.newPlot('candlestickGraph', data, layout);

          console.log(data)
    })
}

function loadBacktestData(data) {
    for (i in data) {
        // Target the backtest div
       var div = document.getElementById('backtest')
       // Create a paragraph tag
       var p = document.createElement('p')
       var count = 1
       p.innerHTML = "<p id=timeframe"+count +" style='line-height:.5'>" + "Our accuracy score for " + i + " was " + data[i] + "%</p>"
       count = count++
       
       div.appendChild(p) // add the <p> element to the div 
       document.body.appendChild(div)

}
}
