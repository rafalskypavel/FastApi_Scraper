function testField(index) {
    const testUrl = prompt('Введите URL для теста');
    if (!testUrl) return;

    const name = document.getElementById(`field_name_${index}`).value;
    const selector = document.getElementById(`field_selector_${index}`).value;
    const type = document.getElementById(`field_type_${index}`).value;
    const payload = {
        url: testUrl,
        product_card_selector: document.getElementById('product_card_selector').value,
        fields: { [name]: { selector, type } }
    };

    fetch('/test/test-supplier', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        alert(JSON.stringify(data.result, null, 2));
    })
    .catch(error => {
        console.error('Error testing field:', error);
    });
}

function testEditField(index) {
    const testUrl = prompt('Введите URL для теста');
    if (!testUrl) return;

    const name = document.getElementById(`edit_field_name_${index}`).value;
    const selector = document.getElementById(`edit_field_selector_${index}`).value;
    const type = document.getElementById(`edit_field_type_${index}`).value;
    const payload = {
        url: testUrl,
        product_card_selector: document.getElementById('edit_product_card_selector').value,
        fields: { [name]: { selector, type } }
    };

    fetch('/test/test-supplier', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        alert(JSON.stringify(data.result, null, 2));
    })
    .catch(error => {
        console.error('Error testing field:', error);
    });
}
