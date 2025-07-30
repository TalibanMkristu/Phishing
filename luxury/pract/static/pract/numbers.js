async function makeRequest(url, method, body) {
    try {
        let headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'appliction/json',
        };

        if (typeof body === 'string'){
            headers['Content-Type'] = 'application/json'
        };

        if (method.toLowerCase() === 'post'){
            let csrf = document.querySelector('[name=csrfmiddlewaretoken]').value
            headers['X-CSRFToken'] = csrf
        };

        const response = await fetch(url, {
            method: method,
            headers: headers,
            body: body
        });

        // First check if response is OK
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        };

        // Check content type before parsing
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            // console.log('Received data:', data);
            return data;
        } else {
            const text = await response.text();
            console.error('Received non-JSON response:', text);
            throw new Error('Expected JSON but got HTML');
        }
        
    } catch (error) {
        console.error('Fetch error:', error);
        // Handle error in UI
    }
}

async function getNumber(){
    const data = await makeRequest('', 'get')

    let ulLeft = document.getElementById('ul-left');
    let li = document.createElement('li')
    li.addEventListener('click', getFloatNumber)
    li.innerHTML =await data['numbers']
    ulLeft.appendChild(li)

}

async function getFloatNumber(event) {
    let number = event.target.innerText

    let data = await makeRequest(
        '', 
        method='post',
        body=JSON.stringify({
            number: number,
        })
    )
    let ulRight = document.getElementById('ul-right');
    let li = document.createElement('li')
    li.innerText = await data['float']
    ulRight.appendChild(li)
}

const formEl = document.getElementById('prac-form')
formEl.addEventListener('submit',async (event) => {
    event.preventDefault();
    let formData = new FormData(formEl)
    // console.log(formData.get('username'));
    // console.log(formData.get('password'));
    // username = formData.get('username')
    // password = formData.get('password')
    // formData.append(username)
    // formData.append(password)
    for (let [key, value] of formData.entries()){
        console.log(key, ':', value);

    }
    console.log('formdata', formData);
    
    data = await makeRequest(
        '',
        'post',
        formData
    )
    console.log(await data);
    
})



// async function submitForm() {
//     let formData = new FormData(formEl)
//     console.log(formData.get('username'))
//     let data = await makeRequest(
//         '', 
//         method= 'post',
//         body= JSON.stringify({
//             form: formData,
//         })
//     )
//     console.log('Received data:', data)
// }

// formEl.addEventListener('submit', submitForm)