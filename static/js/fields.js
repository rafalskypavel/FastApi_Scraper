function addField() {
    const container = document.getElementById('fields-container');
    const index = container.querySelectorAll('.row').length;
    const fieldRow = document.createElement('div');
    fieldRow.className = 'row mb-3';
    fieldRow.id = `field-row-${index}`;
    fieldRow.innerHTML = `
        <div class="col">
            <input type="text" id="field_name_${index}" class="form-control" required>
        </div>
        <div class="col">
            <input type="text" id="field_selector_${index}" class="form-control" required>
        </div>
        <div class="col">
            <select id="field_type_${index}" class="form-control" required>
                <option value="str">str</option>
                <option value="int">int</option>
                <option value="float">float</option>
            </select>
        </div>
        <div class="col d-flex align-items-end">
            <button type="button" class="btn btn-danger ms-2" onclick="removeField(${index})">Удалить</button>
        </div>
    `;
    container.appendChild(fieldRow);
}

function removeField(index) {
    const fieldRow = document.getElementById(`field-row-${index}`);
    if (fieldRow) {
        fieldRow.remove();
    }
}

function addEditField() {
    const container = document.getElementById('edit-fields-container');
    const index = container.children.length / 4;
    container.innerHTML += `
        <div class="mb-3">
            <label for="edit_field_name_${index}" class="form-label">Название поля:</label>
            <input type="text" id="edit_field_name_${index}" class="form-control" required>
        </div>
        <div class="mb-3">
            <label for="edit_field_selector_${index}" class="form-label">Селектор поля:</label>
            <input type="text" id="edit_field_selector_${index}" class="form-control" required>
        </div>
        <div class="mb-3">
            <label for="edit_field_type_${index}" class="form-label">Тип данных:</label>
            <select id="edit_field_type_${index}" class="form-control" required>
                <option value="str">str</option>
                <option value="int">int</option>
                <option value="float">float</option>
            </select>
        </div>
        <button type="button" class="btn btn-secondary" onclick="testEditField(${index})">Тест</button>
    `;
}

function getFieldsFromContainer(containerId) {
    const container = document.getElementById(containerId);
    const fields = {};
    for (let i = 0; i < container.children.length; i += 4) {
        const name = container.children[i].querySelector('input').value;
        const selector = container.children[i + 1].querySelector('input').value;
        const type = container.children[i + 2].querySelector('select').value;
        fields[name] = { selector, type };
    }
    return fields;
}

function setFieldsToContainer(containerId, fields) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    let fieldIndex = 0;
    for (const [name, details] of Object.entries(fields)) {
        container.innerHTML += `
            <div class="mb-3">
                <label for="edit_field_name_${fieldIndex}" class="form-label">Название поля:</label>
                <input type="text" id="edit_field_name_${fieldIndex}" class="form-control" value="${name}" required>
            </div>
            <div class="mb-3">
                <label for="edit_field_selector_${fieldIndex}" class="form-label">Селектор поля:</label>
                <input type="text" id="edit_field_selector_${fieldIndex}" class="form-control" value="${details.selector}" required>
            </div>
            <div class="mb-3">
                <label for="edit_field_type_${fieldIndex}" class="form-label">Тип данных:</label>
                <select id="edit_field_type_${fieldIndex}" class="form-control" required>
                    <option value="str" ${details.type === 'str' ? 'selected' : ''}>str</option>
                    <option value="int" ${details.type === 'int' ? 'selected' : ''}>int</option>
                    <option value="float" ${details.type === 'float' ? 'selected' : ''}>float</option>
                </select>
            </div>
            <button type="button" class="btn btn-secondary" onclick="testEditField(${fieldIndex})">Тест</button>
        `;
        fieldIndex++;
    }
}
