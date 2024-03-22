// JavaScript 文件或模板中的<script>标签里
document.addEventListener('DOMContentLoaded', function() {
    var deleteButton = document.getElementById('confirmDeleteButton');
    var deleteConfirmationModal = document.getElementById('deleteConfirmationModal');
    deleteConfirmationModal.addEventListener('show.bs.modal', function(event) {
        var button = event.relatedTarget;
        var outfitId = button.getAttribute('data-outfit-id');
        deleteButton.onclick = function() {
            fetch(`/${username}/outfits/${outfitId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),  // 确保你有获取CSRFToken的函数
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({'id': outfitId})
            }).then(response => {
                if (response.ok) {
                    // 删除成功后的处理，例如隐藏模态框，移除装备的元素等
                    // document.querySelector(`.outfit-item[data-outfit-id="${outfitId}"]`).remove();
                    $('#deleteConfirmationModal').modal('hide');
                    window.location.reload();

                }
            });
        };
    });
});

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
