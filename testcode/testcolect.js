
let scheduleData =[];
async function getData() {
    try {
        const response = await fetch('/getactive_mongo');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        scheduleData = data;
        // console.log(scheduleData);

        let tab = '';
        data.forEach(function (user) {
            get_OID = user['_id'].$oid;
            get_OIDtoString = get_OID.toString();
            // console.log(get_OIDtoString);

            tab += `<tr>
                        <td>${user.ssidshow}</td>
                        <td>${user.event}</td>
                        <td>${user.location}</td>
                        <td>${user.ouGroup}</td>
                        <td class="text-success">${user.status}</td>
                        <td>
                            <a href="#" id="${get_OIDtoString}" data-toggle="modal" data-target="#userModal" class="link-offset-2 link-offset-3-hover link-success link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                Detail
                            </a>
                        </td>
                    </tr>`;
        });
        document.getElementById('tbody_data').innerHTML = tab;

        // Check if DataTable instance already exists and destroy it before reinitialising
        if ($.fn.DataTable.isDataTable('#myTable')) {
            $('#myTable').DataTable().destroy();
        }

        $("#myTable").DataTable({
            data: data,
            columns: [
                { data: "ssidshow" },
                { data: "event" },
                { data: "location" },
                { data: "ouGroup" },
                {
                    data: null,
                    render: function (data, type, row) {
                        if (data['status'] == 'Active' || data['status'] == 'active' || data['status'] == 'ACTIVE') {
                            return `<p class="text-success">${data['status']}</p>`;
                        }
                        else {
                            return `<p class="text-danger">${data['status']}</p>`;
                        }
                    },
                },
                {
                    data: null,
                    render: function (data, type, row) {
                        return `<a href="#" id="${data['_id'].$oid.toString()}" data-toggle="modal" data-target="#userModal" class="link-offset-2 link-offset-3-hover link-success link-underline link-underline-opacity-0 link-underline-opacity-75-hover">Detail</a>`;
                    },
                    orderable: false
                },
            ]
        });

    } catch (error) {
        console.error('Error fetching data:', error);
    }
    getDetails();
}
async function getDetails() {
    const getOpID = document.querySelectorAll('.link-offset-2');
    const getDetailURL = "/getdetail_mongo/";

    getOpID.forEach(aLink => {
        aLink.onclick = async function () {
            const objID = aLink.id;
            try {
                const response = await fetch(getDetailURL + objID);
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const data = await response.json();
                // console.log(data+data['status']);
                if (data['status'] == 'Active' || data['status'] == 'active' || data['status'] == 'ACTIVE') {
                    if (data['ouGroup'] != 'none') {
                        let Headcontent = '';
                        let bthDelete = `
                            <button id="btnDelete" type="button" class="btn btn-danger" data-dismiss="modal">Delete</button>
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            `;
                        Headcontent +=
                            `
                        <p><strong>SSIDNAME: </strong> ${data['ssidshow']}</p>
                        <p><strong>EVENT: </strong>${data['event']}</p>
                        <p><strong>LOCATION: </strong>${data['location']}</p>
                        <p><strong>GOU: </strong>${data['ouGroup']}</p>
                        <p><strong>TIME :</strong>${data['enddate']} to ${data['enddate']}</p>
                        `;
                        let userList = '';
                        users = data['users']
                        users.forEach(function (user) {
                            // userList += `<li class="list-group-item d-flex justify-content-around">`;
                            userList +=
                                `
                                <li class="list-group-item d-flex justify-content-between align-items-start">
                                    <div class="ms-2 me-auto">
                                        <div class="fw-bold"><p>name: ${user.name}</p></div>
                                        <p>ID Card: ${user.idcard}</p>
                                        <p>Phone: ${user.phone}</p></li>
    
                                    </div>
                                </li>
                                `;
                        });
                        // console.log(userList);
                        document.getElementById('headcontent').innerHTML = Headcontent;
                        document.getElementById('userList').innerHTML = userList;
                        document.getElementById('mdbtn').innerHTML = bthDelete;
                        btn_delete(data);
                    }
                    else {
                        let bthDelete = `
                            <button id="btnDelete" type="button" class="btn btn-danger" data-dismiss="modal">Delete</button>
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            `;
                        let Headcontent = '';
                        Headcontent +=
                            `
                        <p><strong>SSIDNAME: </strong> ${data['ssidshow']}</p>
                        <p><strong>EVENT: </strong>${data['event']}</p>
                        <p><strong>LOCATION: </strong>${data['location']}</p>
                        <p><strong>GOU: </strong>${data['ouGroup']}</p>
                        <p><strong>TIME :</strong>${data['enddate']} to ${data['enddate']}</p>
                        `;
                        userList = `<li class="list-group-item d-flex justify-content-around"><p>-</p></li>`;;
                        document.getElementById('headcontent').innerHTML = Headcontent;
                        document.getElementById('userList').innerHTML = userList;
                        document.getElementById('mdbtn').innerHTML = bthDelete;
                        btn_delete(data);

                    }
                }
                

            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
    });


}

function btn_delete(data) {
    document.getElementById('btnDelete').addEventListener('click', async function () {
        const confirmed = await Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Yes, delete it!'
        });

        if (confirmed.isConfirmed) {
            try {
                // Perform delete operation here
                // Example: Send a DELETE request to your backend API
                apidelteURL = 'http://localhost:3000/delete_ssid/';
                ssidname = data['ssidshow'];
                ouGroup = data['ouGroup'];
                const response = await fetch(apidelteURL + ssidname, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    // Add headers and body if needed
                    body: JSON.stringify({ ouGroup: ouGroup })

                });

                if (!response.ok) {
                    throw new Error('Failed to delete data');
                }

                // Show success message
                Swal.fire(
                    ssidname,
                    'Your data has been deleted.',
                    'success'
                ).then((result) => {
                    if (result.isConfirmed) {
                        // window.location.reload();
                        getData();
                    }
                })
                // console.log(data['ouGroup']);

                // Optionally update UI after successful deletion
                // Example: Reload data, update table, etc.
                // Example function to update data
            } catch (error) {
                console.error('Error deleting data:', error);
                // Show error message
                Swal.fire(
                    'Error!',
                    'Failed to delete data.',
                    'error'
                );
            }
        }
    });
}



getData();
