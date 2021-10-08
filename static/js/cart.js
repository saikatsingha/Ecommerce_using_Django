var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action =  this.dataset.action
        console.log('productId:',productId,'action:',action)

        console.log('USER', user)
        if (user == 'AnonymousUser'){
            console.log('User is not Authenticated')
        } else {
            console.log('User is Authenticated, sending data...')
        }

    })
}

function updateUserOrder(productId, action){
    var url = '/update_item/'
    console.log('URL:', url)
    fetch(url, {
        method:'POST',
        headers:{
            'content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, action:'action'})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:',data)
    })
}