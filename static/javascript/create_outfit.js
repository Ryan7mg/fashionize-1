
document.addEventListener('DOMContentLoaded', (event) => {
});

function openSelectionModal(type) {
    fetchClothingItems(type, function(items) {
        renderClothingItems(items, type);
        var modal = new bootstrap.Modal(document.getElementById('clothing-selection-modal'));
        modal.show();
    });
}

// 更新关闭模态框的函数
function closeModal() {
    var modal = bootstrap.Modal.getInstance(document.getElementById('clothing-selection-modal'));
    modal.hide();
}


function fetchClothingItems(type, callback) {
    const url = `/${username}/closet/ajax/get_clothing_items/?type=${type}`;
    fetch(url)
        .then(response => response.json())
        .then(data => callback(data))
        .catch(error => console.error('Error fetching clothing items:', error));
}

function renderClothingItems(items, type) {
    const contentDiv = document.getElementById('clothing-selection-content');
    contentDiv.innerHTML = ''; // 清空现有内容
    items.forEach((item, index) => {
        const tempId = `${type}-${index}`; // 生成临时ID
        const itemDiv = document.createElement('div');
        itemDiv.setAttribute('data-temp-id', tempId);
        itemDiv.innerHTML = `${item.name} (Click to select)`; // 假设每个衣物对象有 name 属性
        itemDiv.className = 'clothing-item'; // 添加CSS类以便样式化
        itemDiv.setAttribute('data-type', type); // 确保设置了正确的 data-type 属性
        itemDiv.addEventListener('click', () => selectClothingItem(item, tempId, type));
        contentDiv.appendChild(itemDiv);

        // 为每个项目添加点击事件处理
        itemDiv.addEventListener('click', () => selectClothingItem(item, tempId));
    });
}


function selectClothingItem(item, tempId, type) {

    const imageUrl = `/media/${item.photo}`; // 根据实际情况调整属性名
    closeModal(); // 关闭模态框

    //document.querySelector('.clothing-grid.top').style.backgroundImage = `url('${imageUrl}')`;



     const grid = document.querySelector(`.clothing-grid.${type}`);
    if (grid) {
        grid.style.backgroundImage = `url('${imageUrl}')`;
        grid.style.backgroundSize = 'cover';
        grid.style.backgroundPosition = 'center';
    }else {
         console.error(`Grid not found for type: ${type}`);
    }


    // 更新隐藏的表单字段，以便提交时包含所选衣物的信息
    const hiddenInputName = document.querySelector(`input[name="${type}_name"]`);
    const hiddenInputImage = document.querySelector(`input[name="${type}_image"]`);
    if (hiddenInputName && hiddenInputImage) {
        hiddenInputName.value = item.name; // 使用衣物名称
        hiddenInputImage.value = imageUrl; //
        }
}

