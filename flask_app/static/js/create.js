console.log("hello")

function addBook(event) {
    event.preventDefault()
    console.log('function linked')
    let bookForm = document.querySelector("#add_form")
    let bookTableBody = document.querySelector("#book_table_body")
    console.log(bookForm)
    let formData = new FormData(bookForm)
    fetch('/api/books/create', {
        method: 'post',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        bookTableBody.innerHTML += `
        <tr>
            <td>${data.form.title}</td>
            <td>${data.form.author}</td>
            <td><a href="/books/${data.book_id}/edit">Edit</a> |
                <a href="/books/${data.book_id}/delete">Delete</a>
            </td>
        </tr>
        `
    })
    .catch(err => console.log(err))
}

function editBook(event){
    event.preventDefault()
    console.log("edit Linked")
    let bookForm =document.querySelector('#edit_book')
    let bookTableBody =document.querySelector('#book_info')
    console.log(bookForm)
    let formData = new FormData(bookForm)
    fetch("/books/"+ formData.get('id') +"/update", {
        method:'post',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        bookTableBody.innerHTML += `
        <a href="/books/+ formData.get('id') +/update">Edit</a> |
        <a href="/books/${data.book_id}/delete">Delete</a>
        `
    })
    .then(err => console.log(err))
}