backtest = 'http://127.0.0.1:5000/api/backtest'


let backtest_info = d3.json(backtest).then(function(backtest_data) {
    return backtest_data

})



function displayBacktest() {

    backtest_renderer = document.getElementById('backtest')

    backtest_info.then(function(d) {
        
        for (i in d) {
             // Target the backtest div
            var div = document.getElementById('backtest')
            // Create a paragraph tag
            var p = document.createElement('p')
            var count = 1
            p.innerHTML = "<p id=timeframe"+count +">" + "Our accuracy score for " + i + " was " + d[i] + "%</p>"
            count = count++
            
            div.appendChild(p) // add the <p> element to the div 
            document.body.appendChild(div)

            console.log(d[i])
            
        }
    })

   
    }





displayBacktest()