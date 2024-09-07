document.addEventListener("DOMContentLoaded", function() {
    fetchSuppliers();
});

async function fetchSuppliers() {
    try {
        const response = await fetch('/suppliers/get-urls');
        const data = await response.json();
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
    } catch (error) {
        console.error('Error fetching suppliers:', error);
    }
}

async function deleteSupplier(url) {
    try {
        const response = await fetch(`/suppliers/delete-supplier/${encodeURIComponent(url)}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        alert(data.message);
        fetchSuppliers();
    } catch (error) {
        console.error('Error deleting supplier:', error);
    }
}

function editSupplier(url) {
    fetch(`/suppliers/get-urls`)
        .then(response => response.json())
        .then(data => {
            const settings = data[url];
            document.getElementById('edit_base_url').value = url;
            document.getElementById('edit_start_page').value = settings.start_page;
            document.getElementById('edit_page_param').value = settings.page_param;
            document.getElementById('edit_template_name').value = settings.template_name;
            document.getElementById('edit_urls').value = settings.urls.join('\n');
            document.getElementById('edit_product_card_selector').value = settings.template.product_card_selector;
            setFieldsToContainer('edit-fields-container', settings.template.fields);
            new bootstrap.Modal(document.getElementById('editSupplierModal')).show();
        })
        .catch(error => console.error('Error fetching supplier:', error));
}

async function startScraping(url) {
    try {
        const response = await fetch(`/suppliers/start-scraping/${encodeURIComponent(url)}`, {
            method: 'POST'
        });
        const data = await response.json();
        alert(data.message);
    } catch (error) {
        console.error('Error starting scraping:', error);
    }
}

async function testSupplier(url) {
    const testUrl = prompt('Введите URL для теста', url);
    if (!testUrl) return;

    try {
        const response = await fetch('/suppliers/get-urls');
        const data = await response.json();
        const settings = data[url];
        const payload = {
            url: testUrl,
            product_card_selector: settings.template.product_card_selector,
            fields: settings.template.fields
        };

        const testResponse = await fetch('/test/test-supplier', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const testData = await testResponse.json();
        alert(JSON.stringify(testData.result, null, 2));
    } catch (error) {
        console.error('Error testing supplier:', error);
    }
}

document.getElementById('edit-supplier-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const baseUrl = document.getElementById('edit_base_url').value;
    const startPage = document.getElementById('edit_start_page').value;
    const pageParam = document.getElementById('edit_page_param').value;
    const templateName = document.getElementById('edit_template_name').value;
    const urls = document.getElementById('edit_urls').value.split('\n').map(url => url.trim()).filter(url => url);
    const productCardSelector = document.getElementById('edit_product_card_selector').value;
    const fields = getFieldsFromContainer('edit-fields-container');

    try {
        const response = await fetch(`/suppliers/update-supplier/${encodeURIComponent(baseUrl)}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ base_url: baseUrl, start_page: startPage, page_param: pageParam, template_name: templateName, urls: urls, product_card_selector: productCardSelector, fields: fields })
        });
        const data = await response.json();
        alert(data.message);
        fetchSuppliers();
        new bootstrap.Modal(document.getElementById('editSupplierModal')).hide();
    } catch (error) {
        console.error('Error updating supplier:', error);
    }
});

function setFieldsToContainer(containerId, fields) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="row mb-3">
            <div class="col"><strong>Название поля</strong></div>
            <div class="col"><strong>Селектор поля</strong></div>
            <div class="col"><strong>Тип данных</strong></div>
            <div class="col"></div>
        </div>`;
    let index = 0;
    for (const [name, selector] of Object.entries(fields)) {
        container.innerHTML += `
            <div class="row mb-3" id="field-row-${index}">
                <div class="col">
                    <input type="text" id="edit_field_name_${index}" class="form-control" value="${name}" required>
                </div>
                <div class="col">
                    <input type="text" id="edit_field_selector_${index}" class="form-control" value="${selector}" required>
                </div>
                <div class="col">
                    <select id="edit_field_type_${index}" class="form-control" required>
                        <option value="str">str</option>
                        <option value="int">int</option>
                        <option value="float">float</option>
                    </select>
                </div>
                <div class="col d-flex align-items-end">
                    <button type="button" class="btn btn-secondary" onclick="testEditField(${index})">Тест</button>
                    <button type="button" class="btn btn-danger ms-2" onclick="removeEditField(${index})">Удалить</button>
                </div>
            </div>
        `;
        index++;
    }
}


function addEditField() {
    const container = document.getElementById('edit-fields-container');
    const index = container.querySelectorAll('.row').length - 1;
    container.innerHTML += `
        <div class="row mb-3" id="field-row-${index}">
            <div class="col">
                <input type="text" id="edit_field_name_${index}" class="form-control" required>
            </div>
            <div class="col">
                <input type="text" id="edit_field_selector_${index}" class="form-control" required>
            </div>
            <div class="col">
                <select id="edit_field_type_${index}" class="form-control" required>
                    <option value="str">str</option>
                    <option value="int">int</option>
                    <option value="float">float</option>
                </select>
            </div>
            <div class="col d-flex align-items-end">
                <button type="button" class="btn btn-secondary" onclick="testEditField(${index})">Тест</button>
                <button type="button" class="btn btn-danger ms-2" onclick="removeEditField(${index})">Удалить</button>
            </div>
        </div>
    `;
}

function removeEditField(index) {
    document.getElementById(`field-row-${index}`).remove();
}

function getFieldsFromContainer(containerId) {
    const container = document.getElementById(containerId);
    const rows = container.querySelectorAll('.row');
    const fields = {};
    rows.forEach((row, index) => {
        if (index === 0) return;  // Пропустить строку заголовка
        const name = row.querySelector(`#edit_field_name_${index - 1}`).value;
        const selector = row.querySelector(`#edit_field_selector_${index - 1}`).value;

        // Проверка на None или пустое значение
        if (name && selector) {
            fields[name] = selector;
        } else if (name && !selector) {
            fields[name] = null; // Если selector пустой, задать значение null
        }
        // Если name пустой, пропускаем эту запись
    });
    return fields;
}



