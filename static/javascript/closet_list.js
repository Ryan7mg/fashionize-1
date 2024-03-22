$(document).ready(function() {
    // 当用户打开删除确认模态框时，更新模态框中的按钮的data属性
    $('#deleteConfirmationModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget); // 触发模态框的按钮
        var clothingId = button.data('clothing-id'); // 从按钮中获取衣物ID
        $('#confirmDeleteButton').data('clothing-id', clothingId); // 设置确认删除按钮的data-clothing-id属性
    });

    // 处理确认删除按钮的点击事件
    $('#confirmDeleteButton').click(function() {
        var clothingId = $(this).data('clothing-id'); // 从确认删除按钮获取衣物ID
        var username = window.username; // 从全局变量获取用户名

        // 发送AJAX请求到服务器以删除衣物
        $.ajax({
            url: `/${username}/closet/${clothingId}/delete_ajax/`,
            type: 'POST',
            data: {
                'id': clothingId,
                'csrfmiddlewaretoken': getCookie('csrftoken') // 从cookie获取CSRF token
            },
            success: function(response) {
                // 请求成功，关闭模态框并删除卡片元素
                $('#deleteConfirmationModal').modal('hide');
                $('div.card[data-clothing-id="' + clothingId + '"]').remove();
                location.reload();
            },
            error: function(xhr, status, error) {
                // 处理错误
                console.error("Error: " + error);
                alert("An error occurred while deleting the item.");
            }
        });
    });
   // 当用户打开编辑模态框时，获取衣物数据并预填充到表单
    $('#editModal').on('show.bs.modal', function(event) {

        var button = $(event.relatedTarget); // 触发模态框的按钮
        var clothingId = button.data('clothing-id'); // 从按钮中获取衣物ID
        var card = button.closest('.card'); // 获取按钮所在的卡片元素

        // 从卡片中提取衣物信息
        var name = card.find('.card-title').text(); // 假设卡片标题包含名称
        var type = card.find('.card-type').text(); // 假设有一个元素包含类型，且有.card-type类
        // var imageUrl = card.find('img').attr('src'); // 如果你想要获取图片的URL

        // 预填充模态框中的表单字段
        $('#editForm #clothingName').val(name);
        // $('#editForm #clothingImage').val(imageUrl); // 文件输入通常不能设置值
        $('#editForm #clothingType').val(type.toLowerCase()); // 确保类型与<select>中的<option>值匹配
        $('#editForm #clothingId').val(clothingId);
    });


         $('#saveChangesButton').click(function() {
            var formData = new FormData($('#editForm')[0]);
            var csrftoken = getCookie('csrftoken'); // 使用之前定义的函数来获取 CSRF token
            formData.append('csrfmiddlewaretoken', csrftoken); // 附加 CSRF token 到表单数据中

            // 根据你的 Django URL 配置来构造 URL
            // 注意：这里我们使用 `clothingId` 来替换 URL 中的 `<int:pk>`
            var clothingId = $('#clothingId').val();
            var url = `/${window.username}/closet/${clothingId}/edit/`; // 确保这个 URL 与你的 Django 后端路由相匹配

            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false, // 不处理数据
                contentType: false, // 不设置内容类型
                success: function(response) {
                    // 请求成功后的操作...
                    $('#editModal').modal('hide');
                    location.reload();
                    // 更新页面上的卡片元素...
                },
                error: function(xhr, status, error) {
                    // 请求失败后的操作...
                    alert("An error occurred while updating the item: " + error);
                }
            });

         });
 });

// 从cookie中获取CSRF token的函数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 设置AJAX请求的全局设置，以确保CSRF token被包含在POST请求中
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
