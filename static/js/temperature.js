document.getElementById('stage-select').addEventListener('change', function () {
    const selectedStageId = this.value;
    
    fetch('{% url "update-stage" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: new URLSearchParams({
            'stage_id': selectedStageId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            Swal.fire({
                icon: 'success',
                title: 'Stage Updated',
                text: 'Stage updated to: ' + data.selected_stage
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Update Failed',
                text: 'Failed to update stage: ' + data.message
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the stage.');
    });
});

const serialDataDiv = document.getElementById('serial-data');


document.addEventListener('DOMContentLoaded', function () {
    const socket = new WebSocket('ws://' + window.location.host + '/ws/serial-data/');

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        let temp =document.getElementById('temperature')
        let hum = document.getElementById('humidity')

        temp.innerHTML=''
        temp.textContent = data.temperature

        hum.innerHTML=''
        hum.textContent = data.humidity   

        fetch('{% url "record-data" %}', {
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
        fetch('{% url "alert_log_data" %}')
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                const tableBody = document.querySelector('#alertTable tbody');
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

                // Initialize DataTable
                $('#alertTable').DataTable();
            } else {
                console.error('Unexpected data format:', data);
            }
        })
        .catch(error => console.error('Error fetching alert logs:', error));
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
});
new DataTable('#alertTable')