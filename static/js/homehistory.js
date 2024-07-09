// async function getData() {
//     const record = await fetch('/getusers_mongo');
//     const data = await record.json(); // Await the parsing of the JSON response

//     let tab = '';
//     data.users.forEach(function (user) {
//         tab += `<tr>
//             <a href="">
//             <td>${user.firstName}</td>
//             <td>${user.age}</td>
//             <td>${user.gender}</td>
//             <td>${user.phone}</td>
//             <td>
//             <a href="#" id="${user.id}" class="link-offset-2 link-offset-3-hover link-success link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
//             Detail
//             </a>
//             </td>
//             </a>
//         </tr>`;
//     });
//     document.getElementById('tbody_data').innerHTML = tab;


//     $("#myTable").DataTable({
//         data: data.users,
//         "columns": [
//             { data: "firstName" },
//             { data: "age" },
//             { data: "gender" },
//             { data: "phone" },
//             {
//                 data: null,
//                 render: function (data, type, row) {
//                     return `<a href="#" onclick="getDetails()" id="${row.id}" class="link-offset-2 link-offset-3-hover link-success link-underline link-underline-opacity-0 link-underline-opacity-75-hover">Detail</a>`;
//                 },
//                 orderable: false
//             },
//         ]
//     });


// }

// function getDetails() {
//     detail_link = document.querySelectorAll('.link-offset-2');
//     detail_link.forEach(function (lnk) {
//         lnk.onclick = function (){
//             // console.log(lnk.id)
//             alert('User id = ' + lnk.id);
//         }
//     })
// }
// getData();

async function getData() {
    try {
        const response = await fetch('/getusers_mongo');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        console.log(data);

        let tab = '';
        data.forEach(function (user) {
            tab += `<tr>
                        <td>${user.id}</td>
                        <td>${user.namessid}</td>
                        <td>${user.evenname}</td>
                        <td>${user.location}</td>
                        <td>
                            <a href="#" id="${user.id}" class="link-offset-2 link-offset-3-hover link-success link-underline link-underline-opacity-0 link-underline-opacity-75-hover" onclick="getDetails('${user.id}')">
                                Detail
                            </a>
                        </td>
                    </tr>`;
        });
        document.getElementById('tbody_data').innerHTML = tab;

        $("#myTable").DataTable({
            data: data,
            columns: [
                { data: "id" },
                { data: "namessid" },
                { data: "evenname" },
                { data: "location" },
                {
                    data: null,
                    render: function (data, type, row) {
                        return `<a href="#" id="${data.id}" onclick="getDetails('${data.id}')" class="link-offset-2 link-offset-3-hover link-success link-underline link-underline-opacity-0 link-underline-opacity-75-hover">Detail</a>`;
                    },
                    orderable: false
                },
            ]
        });
        
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function getDetails(userId) {
    alert('Event id = ' + userId);
    // You can perform additional actions here based on the user ID, such as fetching more details or navigating to another page.
}

getData();
