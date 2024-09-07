document.addEventListener("DOMContentLoaded", function() {
    fetchSuppliers();
});

document.getElementById('add-supplier-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const baseUrl = document.getElementById('base_url').value;
    const startPage = document.getElementById('start_page').value;
    const pageParam = document.getElementById('page_param').value;
    const templateName = document.getElementById('template_name').value;
    const urls = document.getElementById('urls').value.split('\n').map(url => url.trim()).filter(url => url);
    const productCardSelector = document.getElementById('product_card_selector').value;
    const fields = getFieldsFromContainer('fields-container');

    fetch('/suppliers/add-supplier', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ base_url: baseUrl, start_page: startPage, page_param: pageParam, template_name: templateName, urls: urls, product_card_selector: productCardSelector, fields: fields })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchSuppliers();
    });
});

function fetchSuppliers() {
    fetch('/suppliers/get-urls')
        .then(response => response.json())
        .then(data => {
            const suppliersList = document.getElementById('suppliers-list');
            suppliersList.innerHTML = '';
            for (const [url, settings] of Object.entries(data)) {
                const li = document.createElement('li');
                li.classList.add('list-group-item');
                li.innerHTML = `
                    <div>
                        <strong>URL:</strong> ${url}<br>
                        <strong>Шаблон:</strong> ${settings.template_name}
                    </div>
                    <button class="btn btn-warning btn-sm float-end" onclick="editSupplier('${url}')">Редактировать</button>
                    <button class="btn btn-danger btn-sm float-end me-2" onclick="deleteSupplier('${url}')">Удалить</button>
                    <button class="btn btn-success btn-sm float-end me-2" onclick="startScraping('${url}')">Запустить Парсинг</button>
                    <button class="btn btn-info btn-sm float-end me-2" onclick="testSupplier('${url}')">Тест</button>
                `;
                suppliersList.appendChild(li);
            }
        })
        .catch(error => console.error('Error fetching suppliers:', error));
}

function startScraping(url) {
    console.log(`Starting scraping for URL: ${url}`);
    fetch(`/scraping/start-scraping/${encodeURIComponent(url)}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error starting scraping:', error);
    });
}
