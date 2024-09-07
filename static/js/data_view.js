document.addEventListener("DOMContentLoaded", function() {
    fetchSuppliers();
});

async function fetchSuppliers() {
    try {
        const response = await fetch('/data-view/suppliers');
        const data = await response.json();
        const supplierList = document.getElementById('supplier-data-list');
        supplierList.innerHTML = '';
        data.suppliers.forEach(supplier => {
            const button = document.createElement('button');
            button.classList.add('list-group-item', 'list-group-item-action');
            button.textContent = supplier;
            button.onclick = () => fetchSupplierData(supplier);
            supplierList.appendChild(button);
        });
    } catch (error) {
        console.error('Error fetching suppliers:', error);
    }
}

async function fetchSupplierData(supplierName) {
    document.getElementById('loading-spinner').style.display = 'block';
    document.getElementById('supplier-data-card').style.display = 'none';
    try {
        const response = await fetch(`/data-view/supplier-data/${encodeURIComponent(supplierName)}`);
        const data = await response.json();
        displaySupplierData(data.data);
    } catch (error) {
        console.error('Error fetching supplier data:', error);
    } finally {
        document.getElementById('loading-spinner').style.display = 'none';
    }
}

function displaySupplierData(data) {
    const tableHeaders = document.getElementById('table-headers');
    const tableBody = document.getElementById('table-body');
    tableHeaders.innerHTML = '';
    tableBody.innerHTML = '';

    if (data.length > 0) {
        // Determine the headers based on the first row of the data
        const headers = Object.keys(data[0]);

        // Set table headers
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            tableHeaders.appendChild(th);
        });

        // Set table rows
        data.forEach(row => {
            const tr = document.createElement('tr');
            headers.forEach(header => {
                const td = document.createElement('td');
                td.textContent = row[header] || ''; // Ensure that even undefined values are handled
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });


        // Initialize DataTable with specific options
        $('#supplier-data-table').DataTable({
            "paging": false,
            "searching": true,
            "ordering": true,
            "info": true,
            "columnDefs": [
                { "visible": true, "targets": '_all' }
            ],
            "language": {
                "search": "Поиск:",
                "lengthMenu": "Показать _MENU_ записей на странице",
                "zeroRecords": "Ничего не найдено",
                "info": "Показано _PAGE_ из _PAGES_",
                "infoEmpty": "Нет доступных записей",
                "infoFiltered": "(отфильтровано из _MAX_ записей)"
            }
        });

        document.getElementById('supplier-data-list').style.display = 'none';
        document.getElementById('supplier-data-card').style.display = 'block';
    }
}

function hideSupplierData() {
    document.getElementById('supplier-data-card').style.display = 'none';
    document.getElementById('supplier-data-list').style.display = 'block';
}
