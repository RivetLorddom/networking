document.addEventListener("DOMContentLoaded", function() {
    
    try {
        logged_username = document.querySelector('#usernametag').innerHTML;
    }
    catch(err) {
        console.log('User not signed in')
        return 1
    }
        
    this_user_username = document.querySelector("#this_user_username").innerHTML;
    if (logged_username === this_user_username) {
        console.log('Same user')
        return 0
    }
    
    const follow_button = document.getElementById("follow_button")
    button_state(this_user_username, logged_username);
    follow_button.addEventListener('click', () => following_unfollowing(this_user_username, logged_username))
})


// state of button
async function button_state(this_user_username, logged_username) {

    await new Promise(r => setTimeout(r, 120));

    let button_text = ''
    fetch(`/user_api/${this_user_username}`)
    .then(response => response.json())
    .then(user_info => {
        console.log(user_info)
        if (user_info['followers'].includes(logged_username)) {
            button_text = "Unfollow"
            follow_button.classList.remove('btn-dark')
            follow_button.classList.add('btn-secondary')
        } else {
            button_text = "Follow"
            follow_button.classList.remove('btn-secondary')
            follow_button.classList.add('btn-dark')
        }
        follow_button.innerHTML = button_text
        document.getElementById('followers_count').innerHTML = user_info['followers_count']
    })
}


// when the button is clicked:
function following_unfollowing(this_user_username, logged_username) {

    fetch(`/user_api/${this_user_username}`)
    .then(response => response.json())
    .then(user_info => {
        let list_of_followers = user_info['followers']
        if (follow_button.innerHTML === 'Follow') {
            follow(this_user_username, logged_username, list_of_followers)
        } else {
            unfollow(this_user_username, logged_username, list_of_followers)
        }
    })
    // refresh the view to match number of followers
    button_state(this_user_username, logged_username)
}


// update list of followers
function follow(this_user_username, logged_username, list_of_followers) {
    list_of_followers.push(logged_username)
    console.log(list_of_followers)
    fetch(`/user_api/${this_user_username}`, {
        method: "PUT",
        body: JSON.stringify({
            followers: list_of_followers,
            // followers_count: 
        })
    })
}


function unfollow(this_user_username, logged_username, list_of_followers) {
    // delate the logged user from the list of followers
    for (var i = 0; i < list_of_followers.length; i++) {
        if (list_of_followers[i] === logged_username) {
            list_of_followers.splice(i, 1);
    }}
    console.log(list_of_followers)

    fetch(`/user_api/${this_user_username}`, {
        method: "PUT",
        body: JSON.stringify({
            followers: list_of_followers
        })
    })
}