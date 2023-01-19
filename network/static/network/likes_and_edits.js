document.addEventListener("DOMContentLoaded", function() {

    try {
        this_username = document.querySelector('#usernametag').innerHTML;
    }
    catch(err) {
        console.log('User not signed in')
    }

    // make like buttons work
    const all_like_buttons = document.querySelectorAll('.like_button')
    all_like_buttons.forEach(function(button) {
        // console.log(button.id)
        likes_state(button.id)
        button.addEventListener('click', () => liking_unliking(button.id))
    })

    // make edit buttons work
    const all_edit_buttons = document.querySelectorAll('.edit_button')
    all_edit_buttons.forEach(function(button) {
        button.addEventListener('click', () => editing(button.id))
    })
    
});

// Get current number of likes from API
async function likes_state(id) {
    
    await new Promise(r => setTimeout(r, 120));

    let like_button_text = ''
    fetch(`/posts/${id}`)
    .then(response => response.json())
    .then(post => {
        // console.log(post)
        if (post['liked_by'].includes(this_username)){
            like_button_text = '👎🏻'
        } else {
            like_button_text = '👍🏻'
        }
        document.getElementById(`${id}`).innerHTML = like_button_text
        document.getElementById(`number${id}`).innerHTML = post['likes']
    })
}



// When the button is clicked...
function liking_unliking(id) {
    // console.log(`i am here for id number ${id}`)
    fetch(`/posts/${id}`)
    .then(response => response.json())
    .then(post => {
        let likers_now = post['liked_by']

        if (document.getElementById(`${id}`).innerHTML === '👍🏻'){
            like(id, likers_now)
        } else {
            unlike(id, likers_now)
        }
    })
    // refresh the view of number of likes
    likes_state(id)
}


// Update number of likes and names of likers

function like(id, likers_now) {
    // check is not liked already
    if (! (likers_now.includes(this_username))) {
        likers_now.push(this_username)
        console.log(likers_now)
        fetch(`/posts/${id}`, {
            method: "PUT",
            body: JSON.stringify({
                likes: likers_now.length,
                liked_by: likers_now
            })
        })
    }
}

function unlike(id, likers_now) {
    // delate the user from the list of likers
    for(var i = 0; i < likers_now.length; i++){ 
        if (likers_now[i] === this_username) { 
            likers_now.splice(i, 1); 
    }}
    console.log(likers_now)
    fetch(`/posts/${id}`, {
        method: "PUT",
        body: JSON.stringify({
            likes: likers_now.length,
            liked_by: likers_now
        })
    })
}


// Edit post
function editing(button_id) {
    id = button_id.slice(4)
    console.log(id)
    content_field = document.getElementById(`content${id}`)
    content_before = content_field.innerHTML
    console.log(content_before)
    content_field.innerHTML = `
        <textarea id="new_content${id}" class="edit-area">${content_before}</textarea>
        <button id="save_button${id}" class="btn btn-dark save_button" type="submit" value="submit">Save</button>`
    document.getElementById(button_id).style.display = 'none'

    document.getElementById(`save_button${id}`).addEventListener('click', (button) => {
        document.getElementById(`save_button${id}`).style.display = 'none'
        content_after = document.getElementById(`new_content${id}`).value
        console.log(`New content is: ${content_after}`)
        save_edit(id, content_after)
        document.getElementById(button_id).style.display = 'block'
    })
}


async function save_edit(id, content_after) {

    fetch(`/posts/${id}`, {
        method: "PUT",
        body: JSON.stringify({
            content: content_after
        })
    })

    await new Promise(r => setTimeout(r, 100));

    fetch(`/posts/${id}`)
    .then(response => response.json())
    .then(post => {
        console.log(`Try to save ${id}`)
        console.log(post)
        document.getElementById(`content${id}`).innerHTML = post['content']
    })
}