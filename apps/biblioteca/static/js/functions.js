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

function submit_with_fetch(url, title, content, parameters, method, callback, token) {
    console.log(parameters)
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    fetch(url, {
                        method: method,
                        body: parameters,
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': token
                            // 'Content-Type': 'application/x-www-form-urlencoded',
                        },
                    })
                        .then(res => res.json())
                        .then(data => {
                            if (!data.hasOwnProperty('error')) {
                                callback();
                            } else {
                                Swal.fire({
                                    title: 'Error!',
                                    text: data['error'],
                                    icon: 'error',
                                })
                            }
                        })
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

const csrftoken = getCookie('csrftoken');
var table;
var modal_title;
var urltem;
const url = "http://127.0.0.1:8000/dashboard/book/";

function load_data(url) {
    table = $(`#table`).DataTable({
        autoWidth: true,
        paginate: true,
        destroy: true,
        deferRender: true,
         ajax: {
            url: url,
            type: 'GET',
            data: {},
            dataSrc: ""
        },
        columns: [
            {"data": 'code'},
            {"data": 'title'},
            {"data": 'author'},
            {"data": 'quantity'},
            {"data": 'id'},


        ],
        columnDefs: [{
            targets: [-1],

            class: "text-center",
            orderable: false,
            render: function (data, type, row) {
                var buttons = '<a class="btn btn-warning btn-xs btn-flat btnAdd" rel="edit"> <i class="fas fa-edit"></i> </a> ';
                return buttons
            }
        },
            {
                targets: [1, 2, 3],
                "searchable": false
            }

        ],
        initComplete: function (settings, json) {

        }
    });
}


$(function () {
    modal_title = $('.modal-title');
    load_data(url);
    $('.btnAdd').on('click', function () {
        document.querySelector('input[name="action"]').value = 'add'
        modal_title.find('span').html('Creación de un Libro');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        document.getElementById("id_code").value = ""
        document.getElementById("id_title").value = ""
        document.getElementById("id_author").value = ""
        document.getElementById("id_quantity").value = ""
        $('#createModal').modal('show');
        console.log($('form'))
        urltem = url
    });

    $('#table tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de un libro');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = table.cell($(this).closest('td, li')).index();
            var valor = table.row(tr.row).data();
            //console.log(document.getElementById("id_author").option)
            document.querySelector('input[name="action"]').value = 'edit'
            let id = valor.id
            document.getElementById("id_code").value = valor['code']
            document.getElementById("id_title").value = valor['title']
            document.getElementById("id_author").value = valor['author']
            /*  let obj = document.getElementById("id_author")
              for (i = 0; i < obj.options.length; i++) {
                  if (obj.options[i].text == valor['author']['name'] + " " + valor["author"]["last_name"]) {
                      obj.selectedIndex = i;
                  }
              }*/
            document.getElementById("id_quantity").value = valor['quantity']
            $('#createModal').modal('show');
            urltem = `${url}${id}/`;
        })
    ;

    $('#createModal').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        let valor = document.getElementById("hide").value
        const data = JSON.stringify({
            "code": document.getElementById("id_code").value,
            "title": document.getElementById("id_title").value,
            "author": document.getElementById("id_author").value,
            //'author': $("#id_author option:selected").text(),
            "quantity": document.getElementById("id_quantity").value,

        })
        let method = valor == 'add' ? "POST" : "PUT"
        submit_with_fetch(urltem, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', data, method, function () {
            $('#createModal').modal('hide');
            table.ajax.reload();
        }, csrftoken);
    });
});