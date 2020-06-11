import Cookies from 'js-cookie';

function cloneObject(obj) {
    return JSON.parse(JSON.stringify(obj));
}

function fetchPost(url, data) {
    const csrftoken = Cookies.get('csrftoken');
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
}

window.Cookies = Cookies;

export {fetchPost, cloneObject};
