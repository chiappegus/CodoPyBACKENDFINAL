document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('productoForm');
    const tableBody = document.getElementById('clientesTable').querySelector('tbody');
    let isUpdating = false;

    //async permite que la función se comporte de manera asíncrona,
    //puede ejecutar operaciones sin bloquear el hilo principal de ejecucion
    const fetchclientes = async () => {
        //luego cambiaremos la url por https://<hostdepanywhere>/clientes
        const response = await fetch('https://chiappegus.pythonanywhere.com/clientes');
        //const response = await fetch('http://localhost:5000/clientes');// promesa: esperar a que se complete la solicitud HTTP
        const clientes = await response.json(); //esperar a que se complete la conversión de la respuesta a JSON
        tableBody.innerHTML = '';
        clientes.forEach(cliente => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${cliente[0]}</td>
                <td>${cliente[1]}</td>
                <td>${cliente[2]}</td>
                <td>${cliente[3]}</td>
                <td>
                    <button onclick="editProducto(${cliente[0]}, '${cliente[1]}', ${cliente[2]}, ${cliente[3]})">Editar_</button>
                    <button onclick="editProducto(${cliente.id}, '${cliente.nombre}', ${cliente.cantidad}, ${cliente.precio})">Editar</button>
                    <button onclick="deleteProducto(${cliente.id})">Eliminar</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    };

    const addProducto = async (cliente) => {
        await fetch('http://localhost:5000/nuevo_producto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cliente)
        });
        fetchclientes();
    };

    const updateProducto = async (id, cliente) => {
        await fetch(`http://localhost:5000/actualizar_producto/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cliente)
        });
        fetchclientes();
    };

    const deleteProducto = async (id) => {
        await fetch(`http://localhost:5000/eliminar_producto/${id}`, {
            method: 'DELETE'
        });
        fetchclientes();
    };

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const id = document.getElementById('productoId').value;
        const nombre = document.getElementById('nombre').value;
        const cantidad = document.getElementById('cantidad').value;
        const precio = document.getElementById('precio').value;
        const producto = { nombre, cantidad, precio };

        if (isUpdating) {
            updateProducto(id, producto);
            isUpdating = false;
        } else {
            addProducto(producto);
        }

        form.reset();
        document.getElementById('productoId').value = '';
    });

    window.editProducto = (id, nombre, cantidad, precio) => {
        document.getElementById('productoId').value = id;
        document.getElementById('nombre').value = nombre;
        document.getElementById('cantidad').value = cantidad;
        document.getElementById('precio').value = precio;
        isUpdating = true;
    };

    window.deleteProducto = (id) => {
        if (confirm('¿Estás seguro de eliminar este producto?')) {
            deleteProducto(id);
        }
    };

    fetchclientes();
});