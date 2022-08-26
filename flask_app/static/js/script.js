console.log("we're connected")
URL = " https://api.goprogram.ai/inspiration"

quoteResultDiv = document.querySelector("#quoteResult")
const p = document.getElementById("myPelement")
fetch(" https://api.goprogram.ai/inspiration")
    .then(response => response.json())
    .then(data => {
        console.log(data)
        quoteResult.innerHTML = `
            <h1>"${data.quote}"</h1>
            <p>- ${data.author}</p>
            `
    })
    .catch(err => console.log(err))






// quoteResultDiv = document.querySelector("#quoteResult")
// const p = document.getElementById("myPelement")
// fetch(" https://api.goprogram.ai/inspiration")
//     .then(response => response.json())
//     .then(data => {
//         console.log(data)
//         quoteResultDiv.innerHTML = `
//             <h1>"${data.quote}"</h1>
//             <p>- ${data.author}</p>
//             `
//     })
//     .catch(err => console.log(err))