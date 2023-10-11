const axios = require('axios');

axios.get('http://localhost:3000')
    .then(response =>{

        console.log('Response Data: ', response.data);
    })
    .catch(error =>{

        console.error('Error: ',error)
    })
