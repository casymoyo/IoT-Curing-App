const socket = new WebSocket('ws://' + window.location.host + '/ws/serial-data/');
    
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        let temp =document.getElementById('temperature')
        let hum = document.getElementById('humidity')

        if(temp && hum){
            temp.innerHTML=''
            temp.textContent = data.temperature

            hum.innerHTML=''
            hum.textContent = data.humidity 
        }

        fetch('/app/api/record/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  
            },
            body: JSON.stringify({
                temperature: data.temperature,
                humidity: data.humidity
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log('Success:', result);
            logs()
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    socket.onclose = function(e) {
        console.error('WebSocket closed unexpectedly');
    };

    function logs(){
        const tableBody = document.querySelector('#alertTable tbody');

        if(tableBody){
            fetch('/app/logs/')
            .then(response => response.json())
            .then(data => {
                if (Array.isArray(data)) {
                    
                    tableBody.innerHTML = '';  
                
                    data.forEach(alert => {
                        const row = document.createElement('tr');
                        
                        let alertClass = '';
                        switch (alert.alert_type) {
                            case 'HIGH':
                                alertClass = 'alert-high';
                                break;
                            case 'MID':
                                alertClass = 'alert-mid';
                                break;
                            case 'LOW':
                                alertClass = 'alert-low';
                                break;
                        }
                        
                        row.className = alertClass;
                        row.innerHTML = `
                            <td class='${alertClass}'>${new Date(alert.timestamp).toLocaleString()}</td>
                            <td class='${alertClass}'>${alert.stage__name || 'N/A'}</td>
                            <td class='${alertClass}'>${alert.alert_type}</td>
                            <td class='${alertClass}'>${alert.description}</td>
                        `;
                        tableBody.appendChild(row);
                    });
    
                } else {
                    console.error('Unexpected data format:', data);
                }
            })
            .catch(error => console.error('Error fetching alert logs:', error));
        }
    }
    logs()

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

