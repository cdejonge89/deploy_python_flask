console.log("we're connected")
// URL = "https://www.googleapis.com/books/v1/volumes?q="


// quote generator
quoteResultDiv = document.querySelector("#quoteResult")
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

// books
function getBook(event) {
    bookResultDiv = document.querySelector("#bookResult")
    bookName = document.querySelector("#bookName").value
    console.log(bookName)
    bookResultDiv.innerhtml = "looking for books.."
    event.preventDefault()
    console.log("form submitted")
    fetch("https://www.googleapis.com/books/v1/volumes?q=" + bookName)
        .then(res => res.json())
        .then(data => {
            console.log(data)
            // bookResultDiv.innerhtml = `
            //     <h1>${data.items}</h1>
            //
            // `
            for (let type of data.items) {
                bookResultDiv.innerHTML += `
                    <div class="bookCard">
                        <div class="left">
                            <img src="${type.volumeInfo.imageLinks.thumbnail}">
                            <p><a href="${type.volumeInfo.previewLink}">Preview</a></p>
                        
                            <form action="/api/books/add", method ='post'>
                                <input type="hidden" name="title" value="${type.volumeInfo.title}">
                                <input type="hidden" name="author" value="${type.volumeInfo.authors}">
                                <button class="add_list">Add to list</button>
                            </form>
                        </div>
                    
                    <div class="right">
                    <h1>${type.volumeInfo.title}</h1>
                    <h2>Author: ${type.volumeInfo.authors}</h2>
                    <p>${type.volumeInfo.description}</p>
                    </div>
                    </div>
            `
            }
        })
        .catch(err => console.log(err))
}
        






